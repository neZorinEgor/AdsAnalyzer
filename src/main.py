from typing import List

import pandas as pd
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import create_model
from redis import asyncio as aioredis

from src.config import settings

import time

from src.mapping.classification import MODEL_MAP, ModelAlgorithm


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
    title="Best Practice FastAPI",
    description="PydanticSettings, Alembic, RedisCache",
    lifespan=lifespan,
    docs_url="/docs",
)

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


# Moc cache
@app.get("/moc-transactions")
@cache(expire=5)
async def long_translation():
    time.sleep(5)
    return {
        "ok": True,
        "message": "Successful test cache at long operations"
    }


@app.post("/ml/classification/create")
async def add_route(endpoint_path: str, algorithm: ModelAlgorithm, dataset: UploadFile, label_name: str):
    """
    Обработчик, который создает другие обработчики.
    """
    # Создание алгоритма и его обучение
    df = pd.read_csv(dataset.file)
    df.dropna(inplace=True)
    model = MODEL_MAP[algorithm](max_iter=1000)
    feature_names = list(df.drop(columns=label_name))
    schema = create_model('DynamicInput', **{name: (float, ...) for name in feature_names})
    model.fit(pd.get_dummies(df[feature_names]), df[label_name])

    # Обработчик, который будет создан клиентом
    async def classification_endpoint(data: List[schema]):
        input_df = pd.DataFrame(data)
        input_df_encoded = pd.get_dummies(input_df, drop_first=True)
        input_df_encoded = input_df_encoded.reindex(columns=model.feature_names_in_, fill_value=0)
        return [
            {
                "predict_class": int(predict),
                "probability": max(probability)
            } for predict, probability in zip(model.predict(input_df_encoded), model.predict_proba(input_df_encoded))]

    app.add_api_route(path=f"/{endpoint_path}", endpoint=classification_endpoint, methods=["POST"])
    app.openapi_schema = None
    return {
        "message": "successful create classification handler",
        "ml_algorithm": f"{model.__class__()}",
        "endpoint_path": f"/{endpoint_path}",
    }
