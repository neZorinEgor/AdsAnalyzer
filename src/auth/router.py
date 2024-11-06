import logging
import random

from fastapi import APIRouter, Depends
from src.auth.dependency import AuthDependency

from src.auth.repository import AuthRepositoryImpl
from src.auth.service import AuthService
from src.auth.schema import (
    JWTTokenInfo,
    LoginUserSchema,
    RegisterUserSchema,
    UserTokenPayloadSchema,
    UserSuccessfulRegisterMessage,
)
from src.notification.service import NotificationService

router = APIRouter()
logger = logging.getLogger("auth.router")


@router.post("/auth/jwt/register", response_model=UserSuccessfulRegisterMessage, status_code=201, tags=["JWT-Auth"])
async def register(
        register_user: RegisterUserSchema,
):
    """
    Endpoint for register user and save this credentials in database
    """
    logger.info(f"Received register request for {register_user.email}")
    new_user_id = await AuthService(AuthRepositoryImpl).register(register_user)
    return UserSuccessfulRegisterMessage(message="Successful register user", user_id=new_user_id)


@router.post("/auth/jwt/login", response_model=JWTTokenInfo, status_code=200, tags=["JWT-Auth"])
async def login(
    login_user: LoginUserSchema,
):
    """
    Endpoint for generate access jwt token for exist user
    """
    logger.info(f"Received logging request for {login_user.email}")
    return await AuthService(AuthRepositoryImpl).login(login_user)


@router.post("/auth/jwt/forgot_password", status_code=200, tags=["JWT-Auth"])
async def forgot_password(user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.not_banned_user)):
    # TODO
    try:
        reset_code = random.randint(100000, 1000000)
        NotificationService.send_email.delay(email_to=user_credentials.email, email_subject="Смена пароля")
        return "OK!"
    except Exception as e:
        return f"Произошла ошибка при отправке письма: {str(e)}"


@router.get(path="/user/me", response_model=UserTokenPayloadSchema, status_code=200, tags=["User"])
async def get_my_credentials(user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.not_banned_user)):
    """
    Example check access jwt token info
    """
    return user_credentials


@router.delete("/user/delete_my_account", tags=["User"])
async def delete_my_account(user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.not_banned_user)):
    # TODO
    return await AuthService(AuthRepositoryImpl).delete_my_account(user_credentials.sub)
