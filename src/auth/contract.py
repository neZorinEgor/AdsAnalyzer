from abc import ABC, abstractmethod

from src.auth.schema import JWTTokenInfoSchema, RegisterUserSchema


class ABCAuthRepository(ABC):
    @abstractmethod
    async def register(self, register_user: RegisterUserSchema) -> int:
        raise NotImplemented("Method `register` not implemented.")

    @abstractmethod
    async def login(self) -> JWTTokenInfoSchema:
        raise NotImplemented("Method `login` not implemented.")
