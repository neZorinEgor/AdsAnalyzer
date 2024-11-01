import logging
from fastapi import APIRouter, Depends
from src.auth.dependency import get_user

from src.auth.repository import AuthRepositoryImpl
from src.auth.schema import LoginUserSchema, RegisterUserSchema, UserSuccessfulRegisterMessage, JWTTokenInfo, \
    DecodeAccessTokenSchema
from src.auth.service import AuthService

router = APIRouter(prefix="/auth/jwt", tags=["JWTAuth"])
logger = logging.getLogger("auth.router")


@router.post("/register", response_model=UserSuccessfulRegisterMessage, status_code=201)
async def register(
        register_user: RegisterUserSchema,
):
    """
    Endpoint for register user and save this credentials in database
    """
    logger.info(f"Received register request for {register_user.email}")
    register_user_id = await AuthService(AuthRepositoryImpl).register(register_user)
    return UserSuccessfulRegisterMessage(message="Successful register user", register_user_id=register_user_id)


@router.post("/login", response_model=JWTTokenInfo, status_code=200)
async def login(
    login_user: LoginUserSchema,
):
    """
    Endpoint for generate access jwt token for exist user
    """
    logger.info(f"Received logging request for {login_user.email}")
    return await AuthService(AuthRepositoryImpl).login(login_user)


@router.post("/forgot_password", status_code=200)
async def forgot_password():
    return "TODO"


@router.get("/get_my_credentials", response_model=DecodeAccessTokenSchema, status_code=200)
async def get_my_credentials(user_credentials: DecodeAccessTokenSchema = Depends(get_user)):
    """
    Example check access jwt token info
    """
    return user_credentials
