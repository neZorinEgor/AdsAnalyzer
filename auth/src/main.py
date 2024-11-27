import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.utils import init_admin
from src.auth.router import router as auth_router
from src.settings import settings

# Logging configurations
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] [%(asctime)s] [%(name)s] [%(message)s]')
logger = logging.getLogger(__name__)


# Event manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Init admin account")
    await init_admin(email=settings.INITIAL_ADMIN_EMAIL, password=settings.INITIAL_ADMIN_PASSWORD)
    yield
    pass

app = FastAPI(
    title="📚 TrainME",
    description="`No-code` platform for automating the process of building and deploying machine learning models ",
    lifespan=lifespan,
    docs_url="/docs",
    version="1.0.0",
)

# Origins url's for CORS
origins = ["*"]

# Cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth_router)

