from copy import deepcopy

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.ml_endpoint.background import create_clf_handler
from src.ml_endpoint.mapped import ModelAlgorithm
from src.app import app

router = APIRouter()


@router.post("/ml_endpoint/classification/create", tags=["Classifications-Handlers"])
async def create_clf_router(
        endpoint_path: str,                # Путь до обработчика пользователя
        algorithm: ModelAlgorithm,         # Алгоритм машинного обучения
        label_name: str,                   # Имя целевой переменной в dataset
        background: BackgroundTasks,       # Создание и обучение алгоритма на задний фон
        dataset: UploadFile = File(...),   # Данные, на которых обучается алгоритм
        session: AsyncSession = Depends(get_session)
):
    background.add_task(create_clf_handler, endpoint_path, algorithm, deepcopy(dataset), label_name, app, session)
    return {
        "message": "Обработчик создается в фоновом режиме, ожидайте",
        "endpoint_path": f"/{endpoint_path}",
    }


@router.get("/ml_endpoint/classification")
async def read_clf_routers():
    ...


@app.delete("/ml_endpoint/classification/{router_path}", tags=["Classifications-Handlers"])
async def delete_clf_route(router_path: str):
    app.router.routes = [route for route in app.router.routes if route.path != "/predict"]
    app.openapi_schema = None
    app.setup()
    return {"message": f"Путь {router_path} удален."}
