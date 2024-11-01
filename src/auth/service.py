from src.auth.contract import ABCAuthRepository
from src.auth.schema import RegisterUserSchema, LoginUserSchema, JWTTokenInfo
from src.auth.utils import encode_jwt


class AuthService:
    def __init__(self, repository):
        self.__repository: ABCAuthRepository = repository()

    async def register(self, register_user: RegisterUserSchema):
        register_user_id: int = await self.__repository.register(register_user)
        return register_user_id

    async def login(self, login_user: LoginUserSchema):
        user_credentials = await self.__repository.login(login_user)
        jwt_payload = {
            "sub": user_credentials.id,
            "email": user_credentials.email,
        }
        token = encode_jwt(payload=jwt_payload)
        return JWTTokenInfo(access_token=token, token_type="Bearer")
