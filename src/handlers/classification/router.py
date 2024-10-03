from copy import deepcopy

from fastapi import APIRouter, UploadFile, File, BackgroundTasks

from src.handlers.classification.background import create_clf_handler
from src.handlers.classification.mapped import ModelAlgorithm
from src.app import app

router = APIRouter()


@router.post("/ml/classification/create", tags=["Classifications-Handlers"])
async def create_clf_router(
        endpoint_path: str,               # Путь до обработчика пользователя
        algorithm: ModelAlgorithm,        # Алгоритм машинного обучения
        label_name: str,                  # Имя целевой переменной в dataset
        background: BackgroundTasks,      # Создание и обучение алгоритма на задний фон
        dataset: UploadFile = File(...)   # Данные, на которых обучается алгоритм
):
    background.add_task(create_clf_handler, endpoint_path, algorithm, deepcopy(dataset), label_name, app)
    return {
        "message": "Обработчик создается в фоновом режиме.",
        "endpoint_path": f"/{endpoint_path}",
    }


@app.delete("/ml/classification/{router_path}", tags=["Classifications-Handlers"])
async def delete_clf_route(router_path: str):
    app.router.routes = [route for route in app.router.routes if route.path != "/predict"]
    app.openapi_schema = None
    app.setup()
    return {"message": f"Путь {router_path} удален."}
