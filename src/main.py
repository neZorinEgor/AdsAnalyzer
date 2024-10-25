from src.instance import app
from src.classifications.router import router as classification_router
from src.user.router import router as user_router
from src.frontend.router import router as frontend_router


app.include_router(frontend_router)
app.include_router(classification_router)
app.include_router(user_router)


# @app.get("/moc-transactions", tags=["Cache"])
# @cache(expire=5)
# async def long_translation():
#     time.sleep(5)
#     return {
#         "ok": True,
#         "message": "Successful test cache at long operations"
#     }
