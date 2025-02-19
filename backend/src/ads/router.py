from fastapi import APIRouter

router = APIRouter(prefix="/analysis", tags=["ADS"])


@router.post("/upload")
async def analysis_feedback():
    pass
