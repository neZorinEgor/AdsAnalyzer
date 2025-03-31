import datetime
from io import BytesIO
from uuid import uuid4

import requests
from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.ads.dependency import ads_token, user_payload

from src.ads.repository import ADSInfoRepository
from src.ads.schemas import Message
from src.ads.service import AutoAnaalyzerService
from src.brocker import producer
from src.filestorage import s3_client
from src.settings import settings

router = APIRouter(prefix="/ads", tags=["ADS"])


@router.post("/report")
async def send_message_for_analyze_company(
    report_id: int,
    uuid: str = str(uuid4()),
    token: str | None = Depends(ads_token),
    payload: dict = Depends(user_payload)
):
    message = Message(
        uuid=uuid,
        report_id=report_id,
        yandex_id_token=token,
        report_name=f"{datetime.datetime.now(datetime.UTC)}"
    )
    producer.send(topic=settings.ANALYSIS_TOPIC, value=message.__dict__)
    producer.flush()
    await ADSInfoRepository.save_asd_report_info(
        user_email=payload.default_email,
        report_id=report_id,
        is_ready=False,
    )
    return message


@router.get("/paginate")
async def ads_report_pagination(
    limit: int,
    offset: int,
    payload: dict = Depends(user_payload)
):
    return await ADSInfoRepository.get_ads_report_paginate(limit=limit, offset=offset, user_email=payload.default_email)


@router.get("/{report_id}")
async def get_full_report_information(
    report_id: int,
    payload: dict = Depends(user_payload)
):
    report_info = await ADSInfoRepository.get_report_by_id(report_id=report_id, user_email=payload.default_email)
    clustered_df = await s3_client.get_file(bucket=settings.S3_BUCKETS, key=report_info.path_to_clustered_df)
    clustered_df = pd.read_csv(filepath_or_buffer=BytesIO(clustered_df))
    clustered_df.drop(columns=["Unnamed: 0"], inplace=True)
    impact_df = await s3_client.get_file(bucket=settings.S3_BUCKETS, key=report_info.path_to_impact_df)
    impact_df = pd.read_csv(filepath_or_buffer=BytesIO(impact_df))
    return {
        f"bad_segments": f"{report_info.bad_segments}",
        "clustered_df": clustered_df.to_json(force_ascii=False, orient='records'),
        "impact_df": impact_df.to_json(force_ascii=False, orient='records')
    }


@router.post(path="/companies")
def my_companies(token: str | None = Depends(ads_token)):
    url = "https://api.direct.yandex.com/json/v5/campaigns"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept-Language': f'ru'
    }
    payload = {
        "method": "get",
        "params": {
            "SelectionCriteria": {
            },
            "TextCampaignSearchStrategyPlacementTypesFieldNames": ["SearchResults", "ProductGallery", "DynamicPlaces"],
            "FieldNames": [
                "Name",
                "DailyBudget",
                "Funds",
                "Type",
                "Id"
            ],
            "TextCampaignFieldNames": [
                "CounterIds",
                "RelevantKeywords",
                "BiddingStrategy"
            ],
            "SmartCampaignFieldNames": ["Settings"]
        }
    }
    data = requests.post(url=url, headers=headers, json=payload)
    return data.json()["result"]["Campaigns"]


@router.post("/upload")
async def analyze_company(company_df: UploadFile = File()):
    # Preprocessing yandex direct dataframe
    company_df = pd.read_csv(company_df.file, sep=";", header=3)
    company_df.replace({',': '.'}, regex=True, inplace=True)
    company_df.replace({'-': -1}, regex=False, inplace=True)
    company_df["Дата"] = pd.to_datetime(company_df["Дата"], format="%d.%m.%Y")
    ignored_cols = ["№ Группы"]
    for col in company_df.drop(columns=["Дата"]).columns:
        try:
            if col in ignored_cols:
                continue
            isinstance(float(company_df[col][0]), float)
            company_df[col] = company_df[col].astype("float64")
        except ValueError:
            continue
    # Analyzer
    company_analyzer = AutoAnaalyzerService(
        repository=ADSInfoRepository,
        company=company_df,
        optimality_threshold=11,
        scaler=StandardScaler
    )
    return await company_analyzer.analysis()
