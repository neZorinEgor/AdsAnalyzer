from fastapi import APIRouter
from src.auth.repository import AuthRepositoryImpl
from src.auth.schema import LoginUserSchema, RegisterUserSchema
from src.auth.service import AuthService

router = APIRouter(prefix="/auth/jwt", tags=["JWTAuth"])


@router.post("/register")
async def register(
        register_user: RegisterUserSchema,
):
    register_user_id = await AuthService(AuthRepositoryImpl).register(register_user)
    return register_user_id


@router.post("/login")
async def login(
    login_user: LoginUserSchema,
):
    pass
