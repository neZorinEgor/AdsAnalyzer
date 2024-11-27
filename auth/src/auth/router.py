import logging

from fastapi import APIRouter, Depends
from pydantic import EmailStr, constr

from src.auth.dependency import AuthDependency

from src.auth.repository import AuthRepositoryImpl
from src.auth.service import AuthService
from src.auth.schemas import (
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
) -> JWTTokenInfo:
    """
    Endpoint for generate access jwt token for exist user
    """
    logger.info(f"Received logging request for {login_user.email}")
    return await AuthService(AuthRepositoryImpl).login(login_user)


@router.post("/auth/jwt/refresh", response_model=JWTTokenInfo, response_model_exclude_none=True, tags=["JWT-Auth"])
async def refresh_jwt(
        user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user_for_refresh),
) -> JWTTokenInfo:
    return await AuthService(AuthRepositoryImpl).refresh_jwt(user_credentials)


@router.post("/auth/jwt/forgot_password", tags=["JWT-Auth"])
async def forgot_password(user_email: EmailStr):
    """
    Send a message on user email if user exist
    """
    await AuthService(AuthRepositoryImpl).forgot_password(email=user_email)
    return {
        "detail": f"Send message on {user_email}. "
                  f"If you have entered the wrong address, you should repeat the procedure."
    }


@router.put("/user/reset_password", tags=["User"])
async def reset_password(token: str, new_password: constr(min_length=8)):
    """
    Reset password from user email token
    """
    await AuthService(AuthRepositoryImpl).reset_password(token=token, new_password=new_password)


@router.get(path="/user/me", response_model=UserTokenPayloadSchema, status_code=200, tags=["User"])
async def get_my_credentials(user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)):
    """
    Example check access jwt token info
    """
    return user_credentials


@router.delete("/user/delete_my_account", tags=["User"])
async def delete_my_account(user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)):
    """
    Delete current user account from app
    """
    return await AuthService(AuthRepositoryImpl).delete_my_account(user_credentials.sub)


@router.post("/admin/ban/{user_email}", tags=["Admin"])
async def ban_user_by_email(
        user_email: EmailStr,
        user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)
): 
    await AuthService(AuthRepositoryImpl).ban_user_by_email(email_for_ban=user_email, producer=user_credentials)
    return {
        "detail": f"User {user_email} successful banned"
    }


@router.post("/admin/unban/{user_email}", tags=["Admin"])
async def unban_user_by_email(
        user_email: EmailStr,
        user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)
):
    await AuthService(AuthRepositoryImpl).unban_user_by_email(email_for_unban=user_email, producer=user_credentials)
    return {
        "detail": f"User {user_email} successful unbanned"
    }

