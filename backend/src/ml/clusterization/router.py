import logging

from fastapi import APIRouter, UploadFile, File, Depends

from src.auth.dependency import AuthDependency
from src.auth.schemas import UserTokenPayloadSchema
from src.ml.clusterization.repository import MLRepository
from src.ml.clusterization.service import MLService

router = APIRouter(prefix="/ml/clusterization")
logger = logging.getLogger("auth.router")


@router.post(path="/create", tags=["Clusterization"])
async def create_clusterization_model(
        endpoint_path: str,
        dataset: UploadFile = File(...),
        user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)
):
    """
    Endpoint for create clusterization endpoint
    """
    logger.info(f"Received request for create clusterization model by {user_credentials.email}")
    await MLService(MLRepository).create_clusterization_model(
        owner=user_credentials.sub,
        endpoint_path=endpoint_path,
        dataset=dataset
    )


@router.post(path="/predict", tags=["Clusterization"])
async def predict():
    pass
