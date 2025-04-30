import base64
import logging
from contextlib import asynccontextmanager

import requests
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from src.ads.router import router as ads_router
from src.settings import settings

# Logging configurations
logging.basicConfig(level=logging.INFO, )


# Event manager
@asynccontextmanager
async def lifespan(application: FastAPI):
    yield
    pass


limiter = Limiter(key_func=get_remote_address, default_limits=["10/minutes"])
app = FastAPI(
    title="📰 AdsAnalyzer",
    description="Platform for managing and analyzing the effectiveness of advertising campaigns using machine learning and data analysis methods",
    lifespan=lifespan,
    docs_url="/docs",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

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


@app.get("/callback")
async def callback(
    code: str,
):
    auth_string = f"{settings.CLIENT_ID}:{settings.CLIENT_SECRET}".encode('utf-8')
    auth_b64 = base64.b64encode(auth_string).decode('utf-8')
    result = requests.post(
        url="https://oauth.yandex.ru/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_b64}"
        }
    )
    if "error" not in result:
        return result.json().get("access_token")

# Application routers
app.include_router(ads_router)
