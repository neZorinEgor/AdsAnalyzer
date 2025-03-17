from fastapi import APIRouter, UploadFile, File
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.ads.repository import ADSInfoRepository
from src.ads.service import AnalysisServie

router = APIRouter(prefix="/ads", tags=["ADS"])


@router.post("/upload")
async def analyze_company(company_df: UploadFile = File()):
    # Preprocessing yandex direct dataframe
    sample_df = pd.read_csv(company_df.file, sep=";", header=3)
    sample_df.replace({',': '.'}, regex=True, inplace=True)
    sample_df.replace({'-': -1}, regex=False, inplace=True)
    sample_df["Дата"] = pd.to_datetime(sample_df["Дата"], format="%d.%m.%Y")
    ignored_cols = ["№ Группы"]
    for col in sample_df.drop(columns=["Дата"]).columns:
        try:
            if col in ignored_cols:
                continue
            isinstance(float(sample_df[col][0]), float)
            sample_df[col] = sample_df[col].astype("float64")
        except ValueError:
            continue
    company_analyzer = AnalysisServie(
        repository=ADSInfoRepository,
        company=sample_df,
        optimality_threshold=11,
        scaler=StandardScaler
    )
    return await company_analyzer.analysis()
