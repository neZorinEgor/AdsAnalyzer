import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from celery import Celery
from fastapi.middleware.cors import CORSMiddleware

from src.auth.repository import AuthRepository
from src.auth.router import router as auth_router
from src.ads.router import router as ads_router
from src.auth.service import AuthService
from src.settings import settings
from src.filestorage import s3_client

# Logging configurations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Event manager
@asynccontextmanager
async def lifespan(application: FastAPI):
    # Create S3 Bucket
    await s3_client.create_bucket(bucket_name=settings.S3_BUCKETS)
    await AuthService(AuthRepository).init_admin(
        email=settings.INITIAL_ADMIN_EMAIL,
        password=settings.INITIAL_ADMIN_PASSWORD
    )
    yield
    pass


app = FastAPI(
    title="📰 TrainME",
    description="`No-code` платформа для продвинутого анализа рекламных кампаний",
    lifespan=lifespan,
    docs_url="/docs",
    version="1.0.0",
)
# Broker client for hard CPU tasks
celery = Celery(
    main="celery",
    broker=settings.redis_url,
    broker_connection_retry_on_startup=True
)


# Origins url's for CORS
origins = ["*"]


# Cors middleware
app.add_middleware(
    CORSMiddleware, # noqa
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get(path="/healthcheck", status_code=status.HTTP_200_OK, tags=["Docker"])
def healthcheck():
    return "ok"


# Application routers
app.include_router(auth_router)
app.include_router(ads_router)
