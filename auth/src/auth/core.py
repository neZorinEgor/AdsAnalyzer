from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr, constr

from src.auth.models import UserModel
from src.auth.schemas import RegisterUserSchema


class IAuthRepository(ABC):
    @staticmethod
    @abstractmethod
    async def save_user(user: RegisterUserSchema) -> int:
        raise NotImplemented("Method `save_user` not implemented.")

    @staticmethod
    @abstractmethod
    async def find_user_by_email(email: EmailStr) -> Optional[UserModel]:
        raise NotImplemented("Method `find_user_by_emil` not implemented.")

    @staticmethod
    @abstractmethod
    async def find_user_by_id(user_id: int) -> Optional[UserModel]:
        raise NotImplemented("Method `find_user_by_id` not implemented.")

    @staticmethod
    @abstractmethod
    async def delete_user_by_id(user_id: int):
        raise NotImplemented("Method `delete_user_by_id` not implemented.")

    @staticmethod
    @abstractmethod
    async def reset_password_by_email(email: EmailStr, new_password: str):
        raise NotImplemented("Method `reset_password` not implemented.")

    @staticmethod
    @abstractmethod
    async def ban_user_by_email(email: EmailStr):
        raise NotImplemented("Method `ban_user_by_email` not implemented.")

    @staticmethod
    @abstractmethod
    async def unban_user_by_email(email: EmailStr):
        raise NotImplemented("Method `unban_user_by_email` not implemented.")
