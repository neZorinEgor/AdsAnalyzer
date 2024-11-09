from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError

from src.core.auth.exceptions import InvalidTokenException, ExpiredTokenException, UserIsBlockedException
from src.core.auth.schema import UserTokenPayloadSchema
from src.core.auth.utils import decode_jwt


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
