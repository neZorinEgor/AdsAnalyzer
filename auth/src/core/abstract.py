from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr

from src.core.model import UserModel
from src.core.schema import RegisterUserSchema, NewPassword


class ABCAuthRepository(ABC):
    @staticmethod
    @abstractmethod
    async def save_user(user: RegisterUserSchema) -> int:
        """
        Save new user in `abstract` storage
        """
        raise NotImplemented("Method `save_user` not implemented.")

    @staticmethod
    @abstractmethod
    async def find_user_by_emil(email: EmailStr) -> Optional[UserModel]:
        """
        Get user from `abstract` storage by email
        """
        raise NotImplemented("Method `find_user_by_emil` not implemented.")

    @staticmethod
    @abstractmethod
    async def delete_user_by_id(user_id: int):
        """
        Delete user from `abstract` storage by email
        """
        raise NotImplemented("Method `delete_user_by_id` not implemented.")


    @staticmethod
    @abstractmethod
    async def reset_password(email: EmailStr, new_password: NewPassword):
