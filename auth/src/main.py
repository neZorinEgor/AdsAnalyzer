import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.router import router as auth_router
from src.settings import BASE_DIR


# Event manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    pass
    yield
    pass

app = FastAPI(
    title="JWT-Authentication microservice",
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

# Logging configurations
logging.basicConfig(level=logging.INFO, format='%(levelname)s:     %(asctime)s     %(name)s     %(message)s')
logger = logging.getLogger(__name__)

app.include_router(auth_router)
