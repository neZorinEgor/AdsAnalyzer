from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
import pandas as pd

from src.ads.dependency import preprocessing_service
from src.ads.service import PreprocessingServie, distributed_preprocessing_dataset
from src.auth.dependency import current_user
from src.auth.schemas import UserPayloadSchema

router = APIRouter(prefix="/ads/yd", tags=["ADS"])


@router.post(path="/preprocessing")
async def preprocessing_dataset(
        user: UserPayloadSchema = Depends(current_user),
        company_dataset: UploadFile = File(...),

):
    distributed_preprocessing_dataset.delay(
        dataset_csv=pd.read_csv(company_dataset.file, low_memory=False).to_csv(),
        filename=company_dataset.filename.split(".")[0],
        user_id=user.sub
    )
    return "Task in queue."


@router.get(path="/{report_id}/download")
async def download_report(
        report_id: int,
        service: PreprocessingServie = Depends(preprocessing_service),
        user: UserPayloadSchema = Depends(current_user)

):
    return await service.download_ads_report(owner_id=user.sub, report_id=report_id)
