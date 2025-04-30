import datetime
from io import BytesIO
from uuid import uuid4

# from yandexid import YandexID
import pandas as pd
import requests

from src.ads.core import IADSRepository
from src.ads.exceptions import report_not_founded_error, report_not_ready_error
from src.ads.schemas import AnalysisKafkaMessage
from src.settings import settings
from src.filestorage import s3_client
from src.brocker import producer
from src.utils import get_user_payload


class AdsService:
    # DI&I
    def __init__(self, repository: type[IADSRepository]):
        self.__repository = repository()

    async def generate_report_by_company(self, company_id: int, token: str):
        uuid = str(uuid4())
        message = AnalysisKafkaMessage(
            uuid=uuid,
            company_id=company_id,
            yandex_id_token=token,
            report_name=f"{int(datetime.datetime.now(datetime.UTC).timestamp())}_report"
        )
        producer.send(topic=settings.ANALYSIS_TOPIC, value=message.__dict__)
        producer.flush()
        # payload = YandexID(token).get_user_info_json()
        payload = get_user_payload(token=token)
        await self.__repository.save_asd_report_info(
            user_email=payload.get("default_email"),
            company_id=company_id,
            is_ready=False,
        )
        return message

    async def paginate_user_report(self, limit: int, offset: int, token: str):
        payload = get_user_payload(token=token)
        return await self.__repository.get_ads_report_paginate(limit=limit, offset=offset, user_email=payload.get("default_email"))

    async def get_report_info_by_id(self, report_id: int, token: str):
        payload = get_user_payload(token=token)
        report_info = await self.__repository.get_report_info_by_id(report_id=report_id, user_email=payload.get("default_email"))
        # TODO remove exception
        if report_info is None:
            raise report_not_founded_error
        if not report_info.is_ready:
            raise report_not_ready_error
        clustered_df = await s3_client.get_file(bucket=settings.S3_BUCKETS, key=report_info.path_to_clustered_df)
        clustered_df = pd.read_csv(filepath_or_buffer=BytesIO(clustered_df))
        clustered_df.drop(columns=["Unnamed: 0"], inplace=True)
        impact_df = await s3_client.get_file(bucket=settings.S3_BUCKETS, key=report_info.path_to_impact_df)
        impact_df = pd.read_csv(filepath_or_buffer=BytesIO(impact_df))
        llm_response = await s3_client.get_file(bucket=settings.S3_BUCKETS, key=report_info.path_to_llm_response)
        return {
            f"bad_segments": f"{report_info.bad_segments}",
            "clustered_df": clustered_df.to_json(force_ascii=False, orient='records'),
            "impact_df": impact_df.to_json(force_ascii=False, orient='records'),
            "llm_response": llm_response.decode("utf-8")
        }

    @staticmethod
    async def get_user_companies(token):
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
                "TextCampaignSearchStrategyPlacementTypesFieldNames": [
                    "SearchResults",
                    "ProductGallery",
                    "DynamicPlaces"
                ],
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
        return data.json()
