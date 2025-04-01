import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from yandexid import AsyncYandexOAuth

from src.ads.dependency import ads_token
from src.ads.router import router as ads_router
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
    yield
    pass


app = FastAPI(
    title="📰 AdsAnalyzer",
    description="Platform for managing and analyzing the effectiveness of advertising campaigns using machine learning and data analysis methods",
    lifespan=lifespan,
    docs_url="/docs",
    version="1.0.0",
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


@app.get("/token", tags=["ADS"])
def ads_token(token: str | None = Depends(ads_token)):
    from yandexid import YandexID
    return YandexID(token).get_user_info_json()


@app.get(path="/yandex", tags=["ADS"])
def yandex_oauth():
    return RedirectResponse(f"https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.CLIENT_ID}")


@app.get("/callback")
async def callback(
    code: str,
    response: Response,
):
    payload = await AsyncYandexOAuth(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        redirect_uri="http://127.0.0.1:8000/callback"
    ).get_token_from_code(code)
    print(payload.access_token)
    response.set_cookie("ads_analyzer", payload.access_token, expires=9999999)
    # return RedirectResponse(f"/docs")

# Application routers
# app.include_router(auth_router)
app.include_router(ads_router)
