from fastapi import APIRouter, Depends, UploadFile, File

from src.ads.dependency import preprocessing_service
from src.ads.service import PreprocessingServie

router = APIRouter(prefix="/ads", tags=["ADS"])


@router.post(path="/preprocessing")
async def preprocessing_yandex_direct_dataset(
        company_dataset: UploadFile = File(...),
        service: PreprocessingServie = Depends(preprocessing_service)
):
    return service.__str__()


