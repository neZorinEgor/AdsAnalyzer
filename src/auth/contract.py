from abc import ABC, abstractmethod

from src.auth.schema import RegisterUserSchema, LoginUserSchema, UserCredentialsSchema


class ABCAuthRepository(ABC):
    @abstractmethod
    async def register(self, register_user: RegisterUserSchema) -> int:
        raise NotImplemented("Method `register` not implemented.")

    @abstractmethod
    async def login(self, login_user: LoginUserSchema) -> UserCredentialsSchema:
        raise NotImplemented("Method `login` not implemented.")
