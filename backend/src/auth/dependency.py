from jwt.exceptions import DecodeError, ExpiredSignatureError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.exceptions import (
    invalid_token_exception,
    expired_token_exception,
    invalid_token_type_exception,
    user_is_blocked_exception
)
from src.auth.repository import AuthRepository
from src.auth.schemas import UserPayloadSchema
from src.auth.utils import decode_jwt, TOKEN_TYPE_FIELD, TokenType
from src.auth.service import redis, AuthService

http_bearer = HTTPBearer()


def auth_service():
    return AuthService(repository=AuthRepository)


def __validate_token_type(payload: dict, token_type: TokenType):
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type != token_type:
        raise invalid_token_type_exception


def __get_user_by_token_type(credentials: HTTPAuthorizationCredentials, token_type: TokenType):
    token = credentials.credentials
    try:
        payload = decode_jwt(token)
        if redis.exists(payload.get("email")):
            raise user_is_blocked_exception
        __validate_token_type(payload, token_type)
        return UserPayloadSchema(**payload)
    except DecodeError:
        raise invalid_token_exception
    except ExpiredSignatureError:
        raise expired_token_exception


def current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> UserPayloadSchema:
    """
    Extract and decode the JWT token, returning the user payload.
    """
    return __get_user_by_token_type(credentials, token_type=TokenType.ACCESS)


def current_user_for_refresh(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserPayloadSchema:
    """
    Generate access token by a refresh.
    """
    return __get_user_by_token_type(credentials, token_type=TokenType.REFRESH)
