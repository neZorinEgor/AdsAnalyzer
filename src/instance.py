from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from src.s3.client import s3_client
from src.settings import settings


# Event-Manager
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # Initialize cache and file storage
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # await s3_client.create_bucket()
    # await s3_client.upload_file("docker-compose.yaml")
    yield
    # Shutdown
    await redis.close()
    # await s3_client.close()


app = FastAPI(
    title="TrainMe",
    description="`No-code' platform for automating the process of building and deploying machine learning models",
    lifespan=lifespan,
    docs_url="/docs",
)
app.mount("/static", StaticFiles(directory=Path("src/frontend/static")), name="static")


# Origins url's for CORS
origins = [
    "http://127.0.0.1:5000",
    "https://127.0.0.1:5000",

    "http://0.0.0.0:5000",
    "https://0.0.0.0:5000",

    "http://localhost:5000",
    "https://localhost:5000",

    "http://0.0.0.0:5000/ml_endpoint/classification/",
    "https://0.0.0.0:5000/ml_endpoint/classification/",
]

# Cors settings
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
