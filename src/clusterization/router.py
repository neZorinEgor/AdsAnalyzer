from fastapi import APIRouter, Depends, UploadFile, File
import pandas as pd
from pydantic import create_model

from src.auth.dependency import AuthDependency
from src.auth.schema import UserTokenPayloadSchema
from src.instance import app

router = APIRouter(prefix="/ml/clusterizations")


@router.post("/create")
async def create_clusterization_model(
        endpoint_path: str,
        dataset: UploadFile = File(...),
        user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.not_banned_user),
):
    # Dataset preprocessing
    data_frame = pd.read_csv(dataset.file)
    data_frame.dropna(inplace=True)
    ...

    async def create_clusterization_endpoint():
        ...

    app.add_api_route(
        path=f"/{user_credentials.email}/{endpoint_path}",
        endpoint=create_clusterization_endpoint,
        methods=["POST"],
        tags=[user_credentials.email]
    )
    app.openapi_schema = None
    ...
