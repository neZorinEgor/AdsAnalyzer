from jwt.exceptions import DecodeError, ExpiredSignatureError
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.exceptions import InvalidTokenException, ExpiredTokenException
from src.auth.schema import DecodeAccessTokenSchema
from src.auth.utils import decode_jwt


def get_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    Dependency for read user credentials from access token
    """
    token = credentials.credentials
    try:
        payload = decode_jwt(token)
    except DecodeError:
        raise InvalidTokenException
    except ExpiredSignatureError:
        raise ExpiredTokenException
    return DecodeAccessTokenSchema(**payload)
