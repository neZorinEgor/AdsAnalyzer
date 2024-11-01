from src.auth.contract import ABCAuthRepository
from src.auth.schema import RegisterUserSchema


class AuthService:
    def __init__(self, repository):
        self.__repository: ABCAuthRepository = repository()

    async def register(self, register_user: RegisterUserSchema):
        register_user_id = await self.__repository.register(register_user)
        return register_user_id
