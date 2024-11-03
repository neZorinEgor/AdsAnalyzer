from jwt.exceptions import DecodeError, ExpiredSignatureError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.exceptions import InvalidTokenException, ExpiredTokenException, UserIsBlockedException, UserIsNotSuperException
from src.auth.schema import UserTokenPayloadSchema
from src.auth.utils import decode_jwt


class AuthDependency:
    @staticmethod
    def _get_user_from_token(credentials: HTTPAuthorizationCredentials) -> UserTokenPayloadSchema:
        """
        Extract and decode the JWT token, returning the user payload.
        """
        token = credentials.credentials
        try:
            payload = decode_jwt(token)
        except DecodeError:
            raise InvalidTokenException
        except ExpiredSignatureError:
            raise ExpiredTokenException
        return UserTokenPayloadSchema(**payload)

    @staticmethod
    def not_banned_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """
        Dependency to check if user is not banned.
        """
        user = AuthDependency._get_user_from_token(credentials)
        if user.is_banned:
            raise UserIsBlockedException
        return user

    @staticmethod
    def super_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """
        Dependency to check if user is a superuser.
        """
        user = AuthDependency._get_user_from_token(credentials)
        if not user.is_superuser:
            raise UserIsNotSuperException
        if user.is_banned:
            raise UserIsBlockedException
        return user
