from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pathlib import Path


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