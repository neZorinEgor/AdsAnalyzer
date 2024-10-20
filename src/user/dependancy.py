from typing import Annotated
from fastapi import Cookie
import jwt

from src.config import settings
from src.user.exceptions import token_not_founded_exception, bad_token_exception
from src.user.schema import UserReadInfo
from src.user.utils import decode_jwt


def get_user_credentials_from_token(
    TrainMeJWT: Annotated[str | None, Cookie()] = None
):
    """
    Зависимость для получения модели пользователя
    """
    if not TrainMeJWT:
        raise token_not_founded_exception
    try:
        decode = decode_jwt(TrainMeJWT, public_key=settings.jwt_public_key)
        return UserReadInfo(
            username=decode["username"],
            register_at=decode["register_at"],
            email=decode["email"],
            id=decode["id"],
        )
    except jwt.exceptions.DecodeError:
        raise bad_token_exception
