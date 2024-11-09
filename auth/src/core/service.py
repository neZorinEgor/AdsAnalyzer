import logging

from src.core.abstract import ABCAuthRepository
from src.core.schema import RegisterUserSchema, LoginUserSchema, JWTTokenInfo
from src.core.utils import encode_jwt, check_password
from src.core.exceptions import (
    UserByThisEmailAlreadyExistException,
    InvalidCredentialsException,
    UserIsBlockedException,
)

logger = logging.getLogger("auth.service")


class AuthService:
    def __init__(self, repository):
        # Dependency inversion, so as not to depend on implementation ;)
        self.__repository: ABCAuthRepository = repository()

    async def register(self, new_user: RegisterUserSchema):
        # 1. Check if the user already exists ✅
        exist_user = await self.__repository.find_user_by_emil(new_user.email)
        if exist_user:
            logger.error(f"Try register {new_user.email}, but already exist.")
            raise UserByThisEmailAlreadyExistException
        # 2. Saving the user 💾 (awesome 👍)
        logger.info(f"Successful save new user {new_user.email}")
        new_user_id = await self.__repository.save_user(new_user)
        return new_user_id

    async def login(self, login_user: LoginUserSchema):
        # 1. Verify that the user exists and is submitting the required credentials ✅
        user = await self.__repository.find_user_by_emil(login_user.email)
        if not user or not check_password(login_user.password, user.password.encode()):
            logger.error(f"Try login by invalid credentials: {login_user.email}.")
            raise InvalidCredentialsException
        # 2. Check if the user is banned 🚫
        if user.is_banned:
            raise UserIsBlockedException
        # 3. Issue access JWT token (awesome 👍)
        logger.info(f"{login_user.email} successful login.")
        jwt_payload = {
            "sub": user.id,
            "email": user.email,
            "is_banned": user.is_banned,
            "is_superuser": user.is_superuser
        }
        return JWTTokenInfo(access_token=encode_jwt(payload=jwt_payload), token_type="Bearer")

    async def delete_my_account(self, user_id: int):
        return await self.__repository.delete_user_by_id(user_id)
