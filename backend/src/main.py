from fastapi_cache.decorator import cache

from src.app import app
from src.ml_endpoint.router import router as classification_router
from src.user.router import router as user_router

import time

app.include_router(classification_router)
app.include_router(user_router)


@app.get("/moc-transactions", tags=["Cache"])
@cache(expire=5)
async def long_translation():
    time.sleep(5)
    return {
        "ok": True,
        "message": "Successful test cache at long operations"
    }
