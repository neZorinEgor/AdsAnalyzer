import logging
import random

from fastapi import APIRouter, Depends
from pydantic import EmailStr, constr

from src.core.dependency import AuthDependency

from src.core.repository import AuthRepositoryImpl
from src.core.service import AuthService
from src.core.schema import (
    JWTTokenInfo,
    LoginUserSchema,
    RegisterUserSchema,
    UserTokenPayloadSchema,
    UserSuccessfulRegisterMessage,
)

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


@router.post("/auth/jwt/forgot_password", tags=["JWT-Auth"])
async def forgot_password(user_email: EmailStr):
    await AuthService(AuthRepositoryImpl).forgot_password(email=user_email)
    return {
        "detail": f"Send message on {user_email}. "
                  f"If you have entered the wrong address, you should repeat the procedure."
    }


@router.put("/user/reset_password", tags=["User"])
async def reset_password(token: str, new_password: constr(min_length=8)):
    await AuthService(AuthRepositoryImpl).reset_password(token=token, new_password=new_password)


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
