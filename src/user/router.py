from fastapi import APIRouter

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create")
async def create_user():
    pass
