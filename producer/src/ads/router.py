import requests
from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.ads.dependency import ads_token


from src.ads.repository import ADSInfoRepository
from src.ads.service import AutoAnaalyzerService

router = APIRouter(prefix="/ads", tags=["ADS"])


# @router.get("/token")
# def ads_token(token: str | None = Depends(ads_token)):
#     from yandexid import YandexID
#     return YandexID(token).get_user_info_json()


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
