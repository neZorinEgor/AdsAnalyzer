from jwt.exceptions import DecodeError, ExpiredSignatureError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.exceptions import InvalidTokenException, ExpiredTokenException, InvalidTokenTypeException
from src.core.schema import UserTokenPayloadSchema, UserTokenPayloadSchema
from src.core.utils import decode_jwt, TOKEN_TYPE_FIELD, TokenType

http_bearer = HTTPBearer()


class AuthDependency:
    @staticmethod
    def validate_token_type(payload: dict, token_type: TokenType):
        # TODO check black list
        current_token_type = payload.get(TOKEN_TYPE_FIELD)
        if current_token_type != token_type:
            raise InvalidTokenTypeException

    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> UserTokenPayloadSchema:
        """
        Extract and decode the JWT token, returning the user payload.
        """
        token = credentials.credentials
        try:
            payload = decode_jwt(token)
            # can only be logged in with an access token
            AuthDependency.validate_token_type(payload, TokenType.ACCESS)
            return UserTokenPayloadSchema(**payload)
        except DecodeError:
            raise InvalidTokenException
        except ExpiredSignatureError:
            raise ExpiredTokenException

    @staticmethod
    def get_current_user_for_refresh(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> UserTokenPayloadSchema:
        """
        Extract and decode the JWT token, returning the user payload.
        """
        token = credentials.credentials
        try:
            payload = decode_jwt(token)
            # can only be logged in with an access token
            AuthDependency.validate_token_type(payload, TokenType.REFRESH)
            return UserTokenPayloadSchema(**payload)
        except DecodeError:
            raise InvalidTokenException
        except ExpiredSignatureError:
            raise ExpiredTokenException

    # @staticmethod
    # def not_banned_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    #     """
    #     Dependency to check if user is not banned.
    #     """
    #     user = AuthDependency.get_current_user(credentials)
    #     if user.is_banned:
    #         raise UserIsBlockedException
    #     return user
    #
    # @staticmethod
    # def super_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    #     """
    #     Dependency to check if user is a superuser.
    #     """
    #     user = AuthDependency.get_current_user(credentials)
    #     if not user.is_superuser:
    #         raise UserIsNotSuperException
    #     if user.is_banned:
    #         raise UserIsBlockedException
    #     return user
