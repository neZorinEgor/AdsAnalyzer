from copy import deepcopy

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.classifications.background import create_clf_handler
from src.classifications.mapped import ModelAlgorithm
from src.app import app

router = APIRouter(tags=["Classifications-Handlers"])


@router.post("/ml_endpoint/classification/create")
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

