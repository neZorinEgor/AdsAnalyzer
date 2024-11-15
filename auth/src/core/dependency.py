from jwt.exceptions import DecodeError, ExpiredSignatureError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.exceptions import InvalidTokenException, ExpiredTokenException, InvalidTokenTypeException, UserIsBlockedException
from src.core.schema import UserTokenPayloadSchema
from src.core.utils import decode_jwt, TOKEN_TYPE_FIELD, TokenType
from src.core.service import redis
from src.settings import settings

http_bearer = HTTPBearer()


class AuthDependency:
    @staticmethod
    def __validate_token_type(payload: dict, token_type: TokenType):
        # TODO check black list
        current_token_type = payload.get(TOKEN_TYPE_FIELD)
        if current_token_type != token_type:
            raise InvalidTokenTypeException

    @staticmethod
    def __get_user_by_token_type(credentials: HTTPAuthorizationCredentials, token_type: TokenType):
        token = credentials.credentials
        try:
            payload = decode_jwt(token)
            if payload.get("is_banned") or redis.get(payload.get("email")) == settings.auth.BAN_MESSAGE.encode():
                raise UserIsBlockedException
            AuthDependency.__validate_token_type(payload, token_type)
            return UserTokenPayloadSchema(**payload)
        except DecodeError:
            raise InvalidTokenException
        except ExpiredSignatureError:
            raise ExpiredTokenException

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
