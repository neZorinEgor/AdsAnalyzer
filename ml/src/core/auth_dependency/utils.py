import jwt
from enum import StrEnum

from src.settings import settings

TOKEN_TYPE_FIELD = "type"


class TokenType(StrEnum):
    REFRESH = "refresh"
    ACCESS = "access"


def decode_jwt(
        jwt_token: str,
        public_key: str = settings.auth.PUBLIC_JWT_KEY_PATH.read_text(),
        algorithm: str = settings.auth.ALGORITHM
) -> dict:
    """
    Decode JWT token by public key
    """
    return jwt.decode(jwt=jwt_token, key=public_key, algorithms=[algorithm], options={"verify_exp": True})
