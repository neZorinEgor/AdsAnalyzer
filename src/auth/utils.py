import datetime

import jwt
import bcrypt

from src.settings import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth.private_jwt_key_path.read_text(),
        algorithm: str = settings.auth.algorithm,
        expire_minutes: int = settings.auth.access_token_expire_minutes
):
    now = datetime.datetime.now(datetime.UTC)
    to_encode = payload.copy()
    to_encode.update(
        exp=now + datetime.timedelta(minutes=expire_minutes),
        iat=now,
    )
    return jwt.encode(to_encode, key=private_key, algorithm=algorithm)


def decode_jwt(
        jwt_token: str,
        public_key: str = settings.auth.public_jwt_key_path.read_text(),
        algorithm: str = settings.auth.algorithm
):
    return jwt.decode(jwt=jwt_token, key=public_key, algorithms=[algorithm], options={"verify_exp": True})


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt=salt)


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
