from fastapi import APIRouter, UploadFile, File
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.ads.repository import ADSInfoRepository
from src.ads.service import AutoAnaalyzerService

router = APIRouter(prefix="/ads", tags=["ADS"])


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
    company_analyzer = AutoAnaalyzerService(
        repository=ADSInfoRepository,
        company=company_df,
        optimality_threshold=11,
        scaler=StandardScaler
    )
    return await company_analyzer.analysis()
