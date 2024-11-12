from fastapi import APIRouter

router = APIRouter(prefix="/gateway")


@router.post("/auth/jwt/register", tags=["JWT-Auth"])
async def register():
    pass


@router.post("/auth/jwt/login", tags=["JWT-Auth"])
async def login():
    pass


@router.get("/user/me", tags=["User"])
def get_my_credentials():
    pass


@router.delete("/user/delete_my_account", tags=["User"])
async def delete_my_account():
    pass


@router.post("/user/forgot_password", tags=["User"])
async def forgot_password():
    pass
