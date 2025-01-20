from datetime import timedelta
import datetime

import jwt
import bcrypt
from enum import StrEnum
import uuid

from src.auth.models import UserModel
from src.settings import settings

TOKEN_TYPE_FIELD = "type"


class TokenType(StrEnum):
    REFRESH = "refresh"
    ACCESS = "access"


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth.PRIVATE_JWT_KEY_PATH.read_text(),
        algorithm: str = settings.auth.ALGORITHM,
        expire_timedelta: timedelta = settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES
):
    """
    Encode JWT token by long private key
    """
    now = datetime.datetime.now(datetime.UTC)
    to_encode = payload.copy()
    to_encode.update(
        exp=now + expire_timedelta,
        iat=now,
    )
    return jwt.encode(to_encode, key=private_key, algorithm=algorithm)


def decode_jwt(
        jwt_token: str,
        public_key: str = settings.auth.PUBLIC_JWT_KEY_PATH.read_text(),
        algorithm: str = settings.auth.ALGORITHM
) -> dict:
    """
    Decode JWT token by public key
    """
    return jwt.decode(jwt=jwt_token, key=public_key, algorithms=[algorithm], options={"verify_exp": True})


def hash_password(password: str) -> bytes:
    """
    Hash password by algorithm + salt
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt=salt)


def check_password(password: str, hashed_password: bytes) -> bool:
    """
    Compare input password and hash
    """
    return bcrypt.checkpw(password.encode(), hashed_password)


def create_jwt(
        token_type: str,
        token_data: dict,
        expire_timedelta: timedelta = settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES,

) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(payload=jwt_payload, expire_timedelta=expire_timedelta)


def create_access_token(user: UserModel) -> str:
    print(user.__dict__)
    jwt_payload = {
        "sub": user.id,
        "email": user.email,
        "role": user.role
    }
    return create_jwt(token_type=TokenType.ACCESS, token_data=jwt_payload)


def create_refresh_token(user: UserModel) -> str:
    jwt_payload = {
        "sub": user.id,
        "email": user.email
    }
    return create_jwt(
        token_type=TokenType.REFRESH,
        token_data=jwt_payload,
        expire_timedelta=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS
    )
