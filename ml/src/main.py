from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.core.router import router as ml_router


@asynccontextmanager
async def lifespan(app: FastAPI): # noqa
    yield
    pass


app = FastAPI(
    title="ML-microservice",
    description="...",
    version="1.0",
    lifespan=lifespan,
    docs_url="/docs"
)

app.include_router(ml_router)