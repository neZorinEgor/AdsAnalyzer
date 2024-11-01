from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.instance import app

router = APIRouter(tags=["Frontend"])

templates = Jinja2Templates(directory=Path("src/frontend/templates"))


@router.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/manual")
async def read_root(request: Request):
    return templates.TemplateResponse("manual.html", {"request": request})


@router.get("/models")
async def read_root(request: Request):
    return templates.TemplateResponse("models.html", {"request": request})


# Страницы для создания эндпоинтов
@router.get("/create")
async def read_root(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@router.get("/create/classifications")
async def read_root(request: Request):
    return templates.TemplateResponse("create/classifications.html", {"request": request})


@router.get("/create/clusterizations")
async def read_root(request: Request):
    return templates.TemplateResponse("create/clusterizations.html", {"request": request})


@router.get("/create/regressions")
async def read_root(request: Request):
    return templates.TemplateResponse("create/regression.html", {"request": request})


# Страницы ошибок
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)
    if exc.status_code == 500:
        return templates.TemplateResponse("errors/405.html", {"request": request}, status_code=500)
    return JSONResponse(status_code=404, content={"detail": "not founded"})
