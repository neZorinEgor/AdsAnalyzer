import logging

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from src.auth.dependency import current_user, current_user_for_refresh, auth_service

from src.auth.service import AuthService
from src.auth.schemas import (
    JWTTokenInfo,
    LoginUserSchema,
    RegisterUserSchema,
    UserPayloadSchema,
)

router = APIRouter()
logger = logging.getLogger("auth.router")


@router.post(path="/auth/jwt/register", response_model=JWTTokenInfo, status_code=201, tags=["JWT-Auth"])
async def register(
        register_user: RegisterUserSchema,
        service: AuthService = Depends(auth_service)
) -> JWTTokenInfo:
    """
    Endpoint for register user and save this credentials in database
    """
    return await service.register(register_user)


@router.post(path="/auth/jwt/login", response_model=JWTTokenInfo, status_code=200, tags=["JWT-Auth"])
async def login(
    login_user: LoginUserSchema,
    service: AuthService = Depends(auth_service)
) -> JWTTokenInfo:
    """
    Endpoint for generate access jwt token for exist user
    """
    return await service.login(login_user)


@router.post(path="/auth/jwt/refresh", response_model=JWTTokenInfo, response_model_exclude_none=True, tags=["JWT-Auth"])
async def refresh_jwt(
        user: UserPayloadSchema = Depends(current_user_for_refresh),
        service: AuthService = Depends(auth_service)
) -> JWTTokenInfo:
    return await service.refresh_jwt(user)


@router.get(path="/user/me", response_model=UserPayloadSchema, status_code=200, tags=["User"])
async def get_my_credentials(
        user: UserPayloadSchema = Depends(current_user)
) -> UserPayloadSchema:
    """
    Example check access jwt token info
    """
    return user


@router.delete(path="/user/delete_my_account", tags=["User"])
async def delete_my_account(
        user: UserPayloadSchema = Depends(current_user),
        service: AuthService = Depends(auth_service)
):
    """
    Delete current user account from app
    """
    return await service.delete_my_account(user.email)


@router.post(path="/admin/ban/{user_email}", tags=["Admin"])
async def ban_user_by_email(
        email_for_ban: EmailStr,
        user: UserPayloadSchema = Depends(current_user),
        service: AuthService = Depends(auth_service)
):
    """
    Ban user by email.
    """
    return await service.ban_user_by_email(email_for_ban=email_for_ban, producer=user)


@router.post(path="/admin/unban/{user_email}", tags=["Admin"])
async def unban_user_by_email(
        email_for_unban: EmailStr,
        user: UserPayloadSchema = Depends(current_user),
        service: AuthService = Depends(auth_service)
):
    """
    Unban user by email.
    """
    return await service.unban_user_by_email(email_for_unban=email_for_unban, producer=user)
