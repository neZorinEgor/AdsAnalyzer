from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.decorator import cache

from src.app import app

from src.frontend.pages.router import router as frontend_router
from src.auth.router import router as auth_router
from src.handlers.classification.router import router as classification_router

import time


# Origins url's for CORS
origins = [
    'http://localhost',
    'https://localhost',
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

app.include_router(frontend_router)
app.include_router(auth_router)
app.include_router(classification_router)


@app.get("/moc-transactions", tags=["Cache"])
@cache(expire=5)
async def long_translation():
    time.sleep(5)
    return {
        "ok": True,
        "message": "Successful test cache at long operations"
    }
