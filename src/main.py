import asyncio
from src.classifications.router import router as classification_router
from src.instance import app
from src.s3.client import s3_client
from src.frontend.router import router as frontend_router
from fastapi_cache.decorator import cache
from fastapi import UploadFile
from src.auth.router import router as auth_router


app.include_router(auth_router)
app.include_router(frontend_router)
app.include_router(classification_router)


@app.get("/moc-transactions", tags=["TestUtils"])
@cache(expire=5)
async def long_translation():
    await asyncio.sleep(5)
    return {
        "ok": True,
        "message": "Successful test cache at long operations"
    }


@app.post("/test/upload", tags=["TestUtils"])
async def upload(file: UploadFile):
    await s3_client.upload_file(file)
    return {
        "ok": True,
        "message": f"Successful upload file {file.filename}"
    }
