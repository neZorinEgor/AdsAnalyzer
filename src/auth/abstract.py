from abc import ABC, abstractmethod
from typing import Optional

from pydantic import EmailStr

from src.auth.model import UserModel
from src.auth.schema import RegisterUserSchema


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
