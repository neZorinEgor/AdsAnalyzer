import jwt

from src.settings import settings


def decode_jwt(
        jwt_token: str,
        public_key: str = settings.auth.public_jwt_key_path.read_text(),
        algorithm: str = settings.auth.algorithm
):
    """
    Decode JWT token by public key
    """
    return jwt.decode(jwt=jwt_token, key=public_key, algorithms=[algorithm], options={"verify_exp": True})
