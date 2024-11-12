from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr, constr

from src.core.model import UserModel
from src.core.schema import RegisterUserSchema


class ABCAuthRepository(ABC):
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
    async def delete_user_by_id(user_id: int):
        raise NotImplemented("Method `delete_user_by_id` not implemented.")

    @staticmethod
    @abstractmethod
    async def reset_password(email: EmailStr, new_password: bytes):
        raise NotImplemented("Method `reset_password` not implemented.")
