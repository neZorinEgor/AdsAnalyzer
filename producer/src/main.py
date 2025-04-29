import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from yandexid import YandexOAuth
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.ads.router import router as ads_router
from src.settings import settings
from src.filestorage import s3_client

from pytz import utc

scheduler = AsyncIOScheduler(timezone=utc)

# Logging configurations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sample_cron():
    print("schedule...")


# Event manager
@asynccontextmanager
async def lifespan(application: FastAPI):
    # Create S3 Bucket
    await s3_client.create_bucket(bucket_name=settings.S3_BUCKETS)
    yield
    scheduler.shutdown()


app = FastAPI(
    title="📰 AdsAnalyzer",
    description="Platform for managing and analyzing the effectiveness of advertising campaigns using machine learning and data analysis methods",
    lifespan=lifespan,
    docs_url="/docs",
    version="1.0.0",
)

# Origins url's for CORS
origins = [
    "http://localhost:8501/",
    "https://localhost:8501/",
]


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


# @app.get("/token", tags=["ADS"])
# def ads_token(token: str | None = Depends(ads_token)):
#     from yandexid import YandexID
#     return YandexID(token).get_user_info_json()


@app.get("/callback")
async def callback(
    code: str,
):
    oauth = YandexOAuth(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        redirect_uri="http://localhost:8501/authenticate"
    )
    payload = oauth.get_token_from_code(code)
    return payload.access_token

# Application routers
# app.include_router(auth_router)
app.include_router(ads_router)
