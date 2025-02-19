from fastapi import APIRouter

router = APIRouter(prefix="/ads", tags=["ADS"])


@router.post("/upload")
async def analysis_feedback():
    pass
