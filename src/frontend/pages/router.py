from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/app", tags=["Frontend"])

router.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")


templates = Jinja2Templates(directory="src/frontend/templates")


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
