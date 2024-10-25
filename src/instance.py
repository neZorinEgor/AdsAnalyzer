
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from src.settings import settings
from src.s3.service import S3Client


# Event-Manager
@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    # Initialize cache and file storage
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    s3_client = S3Client(
        access_key=settings.S3_ACCESS_KEY,
        secret_key=settings.S3_SECRET_KEY,
        endpoint_url=f"{settings.S3_HOST}:{settings.S3_PORT}",
        bucket_name=settings.S3_BUCKET_NAME
    )
    await s3_client.create_bucket()
    await s3_client.upload_file("docker-compose.yaml")
    yield
    # Shutdown
    await redis.close()


app = FastAPI(
    title="TrainMe",
    description="`No-code' platform for automating the process of building and deploying machine learning models",
    lifespan=lifespan,
    docs_url="/docs",
)
app.mount("/static", StaticFiles(directory=Path("src/frontend/static")), name="static")


# Origins url's for CORS
origins = [
    "http://127.0.0.1:5500/",
    "https://127.0.0.1:5500/",
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
