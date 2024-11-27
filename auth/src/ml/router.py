import logging

from fastapi import APIRouter, UploadFile, File, Depends

from src.auth.dependency import AuthDependency
from src.auth.schemas import UserTokenPayloadSchema
from src.ml.repository import MLRepository
from src.ml.service import MLService

router = APIRouter(prefix="ml", tags=["ML"])
logger = logging.getLogger("auth.router")


@router.post(path="/clusterization/create")
async def create_clusterization_model(
        endpoint_path: str,
        dataset: UploadFile = File(...),
        user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)
):
    await MLService(MLRepository).create_clusterization_model(endpoint_path=endpoint_path, dataset=dataset)


@router.post(path="/predict")
async def predict():
    pass
