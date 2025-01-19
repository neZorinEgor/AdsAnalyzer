from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr

from src.auth.models import UserModel
from src.auth.schemas import RegisterUserSchema


class IAuthRepository(ABC):
    @staticmethod
    @abstractmethod
    async def save_user(user: RegisterUserSchema) -> int:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def find_user_by_email(email: EmailStr) -> Optional[UserModel]:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def delete_user_by_email(email: EmailStr) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def update_user_by_email(email: EmailStr, **kwargs) -> None:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    async def init_admin(email: EmailStr, password):
        raise NotImplementedError()
