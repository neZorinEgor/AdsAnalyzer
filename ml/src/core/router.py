from fastapi import APIRouter, Depends, UploadFile, File
from copy import deepcopy

from src.core.auth_dependency.schamas import UserTokenPayloadSchema
from src.core.auth_dependency.dependency import AuthDependency
from src.core.service import MLService


router = APIRouter(prefix="/ml")


@router.get("/me")
def me(user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)):
    return user_credentials


@router.post("/clusterizations")
def create_clusterizations(
        endpoint_path: str,
        dataset: UploadFile = File(...)
):
    MLService(repository="asd").crete_clusterizations(endpoint_path=endpoint_path, dataset=dataset)
