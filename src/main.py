from copy import deepcopy

from fastapi import FastAPI, UploadFile, BackgroundTasks, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from fastapi.staticfiles import StaticFiles

from src.frontend.pages.router import router as frontend_router
from src.ml.background import create_clf_handler
from src.ml.mapped import ModelAlgorithm
from src.config import settings

import time


# Event-Manager
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # Startup
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # Shutdown
    await redis.close()


app = FastAPI(
    title="TrainMe",
    description="`No-code` платформа для автоматизации процессов построения и развертывания моделей машинного обучения с возможностью использования пользователями, не обладающими знаниями программирования ",
    lifespan=lifespan,
    docs_url="/docs",
)

app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Origins url's for CORS
origins = [
    'http://localhost',
    'https://localhost',
]

# Cors settings
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(frontend_router)


# Moc cache
@app.get("/moc-transactions", tags=["Test cache"])
@cache(expire=5)
async def long_translation():
    time.sleep(5)
    return {
        "ok": True,
        "message": "Successful test cache at long operations"
    }


@app.post("/ml/classification/create", tags=["Create Router"])
async def add_classification_router(
        endpoint_path: str,                      # Путь до обработчика пользователя
        algorithm: ModelAlgorithm,               # Алгоритм машинного обучения
        label_name: str,                         # Имя целевой переменной в dataset
        background: BackgroundTasks,             # Создание и обучение алгоритма на задний фон
        dataset: UploadFile = File(...),         # Данные, на которых обучается алгоритм
):
    """
    Обработчик, который создает другие обработчики.
    """
    background.add_task(create_clf_handler, endpoint_path, algorithm, deepcopy(dataset), label_name, app)
    return {
        "message": "Обработчик создается в фоновом режиме.",
        "endpoint_path": f"/{endpoint_path}",
    }
