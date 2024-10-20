
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from src.config import settings


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
app.mount("/static", StaticFiles(directory=Path("src/frontend/static")), name="static")


# Origins url's for CORS
origins = [
    "http://127.0.0.1:5500/",
    "https://127.0.0.1:5500/",
    "*"
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
