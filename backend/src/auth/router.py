import logging

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from src.auth.dependency import AuthDependency

from src.auth.repository import AuthRepository
from src.auth.service import AuthService
from src.auth.schemas import (
    JWTTokenInfo,
    LoginUserSchema,
    RegisterUserSchema,
    UserTokenPayloadSchema,
)

router = APIRouter()
logger = logging.getLogger("auth.router")


@router.post(path="/auth/jwt/register", response_model=JWTTokenInfo, status_code=201, tags=["JWT-Auth"])
async def register(
        register_user: RegisterUserSchema,
) -> JWTTokenInfo:
    """
    Endpoint for register user and save this credentials in database
    """
    return await AuthService(repository=AuthRepository).register(register_user)


@router.post(path="/auth/jwt/login", response_model=JWTTokenInfo, status_code=200, tags=["JWT-Auth"])
async def login(
    login_user: LoginUserSchema,
) -> JWTTokenInfo:
    """
    Endpoint for generate access jwt token for exist user
    """
    return await AuthService(repository=AuthRepository).login(login_user)


@router.post(path="/auth/jwt/refresh", response_model=JWTTokenInfo, response_model_exclude_none=True, tags=["JWT-Auth"])
async def refresh_jwt(
        user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user_for_refresh),
) -> JWTTokenInfo:
    return await AuthService(repository=AuthRepository).refresh_jwt(user_credentials)


@router.get(path="/user/me", response_model=UserTokenPayloadSchema, status_code=200, tags=["User"])
async def get_my_credentials(user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)):
    """
    Example check access jwt token info
    """
    return user_credentials


@router.delete(path="/user/delete_my_account", tags=["User"])
async def delete_my_account(user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)):
    """
    Delete current user account from app
    """
    return await AuthService(repository=AuthRepository).delete_my_account(user_credentials.email)


@router.post(path="/admin/ban/{user_email}", tags=["Admin"])
async def ban_user_by_email(
        email_for_ban: EmailStr,
        user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)
):
    """
    Ban user by email.
    """
    return await AuthService(repository=AuthRepository).ban_user_by_email(email_for_ban=email_for_ban, producer=user_credentials)


@router.post(path="/admin/unban/{user_email}", tags=["Admin"])
async def unban_user_by_email(
        email_for_unban: EmailStr,
        user_credentials: UserTokenPayloadSchema = Depends(AuthDependency.get_current_user)
):
    """
    Unban user by email.
    """
    return await AuthService(repository=AuthRepository).unban_user_by_email(email_for_unban=email_for_unban, producer=user_credentials)
