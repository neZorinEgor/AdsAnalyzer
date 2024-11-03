from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr

from src.auth.model import UserModel
from src.auth.schema import RegisterUserSchema, LoginUserSchema, UserCredentialsSchema


class ABCAuthRepository(ABC):
    @staticmethod
    @abstractmethod
    async def save_user(user: RegisterUserSchema) -> int:
        raise NotImplemented("Method `save_user` not implemented.")

    @staticmethod
    @abstractmethod
    async def find_user_by_emil(email: EmailStr) -> Optional[UserModel]:
        raise NotImplemented("Method `find_user_by_emil` not implemented.")
