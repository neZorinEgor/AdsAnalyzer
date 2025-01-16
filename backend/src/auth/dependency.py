from jwt.exceptions import DecodeError, ExpiredSignatureError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.exceptions import invalid_token_exception, expired_token_exception, invalid_token_type_exception, user_is_blocked_exception
from src.auth.schemas import UserTokenPayloadSchema
from src.auth.utils import decode_jwt, TOKEN_TYPE_FIELD, TokenType
from src.auth.service import redis

http_bearer = HTTPBearer()


class AuthDependency:
    @staticmethod
    def __validate_token_type(payload: dict, token_type: TokenType):
        current_token_type = payload.get(TOKEN_TYPE_FIELD)
        if current_token_type != token_type:
            raise invalid_token_type_exception

    @staticmethod
    def __get_user_by_token_type(credentials: HTTPAuthorizationCredentials, token_type: TokenType):
        token = credentials.credentials
        try:
            payload = decode_jwt(token)
            if redis.exists(payload.get("email")):
                raise user_is_blocked_exception
            AuthDependency.__validate_token_type(payload, token_type)
            return UserTokenPayloadSchema(**payload)
        except DecodeError:
            raise invalid_token_exception
        except ExpiredSignatureError:
            raise expired_token_exception

    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> UserTokenPayloadSchema:
        """
        Extract and decode the JWT token, returning the user payload.
        """
        return AuthDependency.__get_user_by_token_type(credentials, token_type=TokenType.ACCESS)

    @staticmethod
    def get_current_user_for_refresh(
            credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
    ) -> UserTokenPayloadSchema:
        """
        Generate access token by a refresh.
        """
        return AuthDependency.__get_user_by_token_type(credentials, token_type=TokenType.REFRESH)
