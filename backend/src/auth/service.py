import logging
from redis import Redis

from celery import Celery
from pydantic import EmailStr

from src.auth.core import IAuthRepository
from src.auth.schemas import RegisterUserSchema, LoginUserSchema, JWTTokenInfo, UserTokenPayloadSchema
from src.auth import utils as jwt_utils
from src.auth.exceptions import (
    user_already_exist_exception,
    invalid_credentials_exception,
    user_is_blocked_exception,
    user_is_not_super_exception
)
from src.auth.utils import create_access_token
from src.settings import settings

logger = logging.getLogger()
# celery = Celery("notifications", broker=settings.redis_url)
redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


class AuthService:
    def __init__(self, repository):
        # Dependency inversion, so as not to depend on implementation ;)
        self.__repository: IAuthRepository = repository()

    async def register(self, new_user: RegisterUserSchema):
        """
        Register user at platform
        """
        # 1. Check if the user already exists
        exist_user = await self.__repository.find_user_by_email(new_user.email)
        if exist_user:
            logger.error(f"Try register {new_user.email}, but already exist.")
            raise user_already_exist_exception
        # 2. Saving the user
        logger.info(f"Successful save new user {new_user.email}")
        await self.__repository.save_user(new_user)
        return await self.login(LoginUserSchema(**new_user.__dict__))

    async def login(self, login_user: LoginUserSchema) -> JWTTokenInfo:
        """
        Validate user and return JWT-Refresh+Access token
        """
        # 1. Verify that the user exists and is submitting the required credentials
        user = await self.__repository.find_user_by_email(login_user.email)
        if not user or not jwt_utils.check_password(login_user.password, user.password.encode()):
            logger.error(f"Try login by invalid credentials: {login_user.email}.")
            raise invalid_credentials_exception
        # 2. Check if the user is banned
        if user.is_banned:
            raise user_is_blocked_exception
        # 3. Issue access JWT token
        logger.info(f"{login_user.email} successful login.")
        access_token = jwt_utils.create_access_token(user)
        refresh_token = jwt_utils.create_refresh_token(user)
        return JWTTokenInfo(access_token=access_token, refresh_token=refresh_token)

    async def refresh_jwt(self, user_credentials: UserTokenPayloadSchema):
        """
        Generate access token by refresh from credentials
        """
        user = await self.__repository.find_user_by_email(user_credentials.email)
        return JWTTokenInfo(access_token=create_access_token(user))

    async def delete_my_account(self, email: EmailStr) -> None:
        """
        Delete current user by token from db
        """
        logger.info(f"User by id: {email} delete account.")
        await self.__repository.delete_user_by_email(email)

    async def ban_user_by_email(self, email_for_ban: EmailStr, producer: UserTokenPayloadSchema):
        producer = await self.__repository.find_user_by_email(producer.email)
        if not producer.is_superuser:
            raise user_is_not_super_exception
        # await self.__repository.ban_user_by_email(email_for_ban)
        await self.__repository.update_user_by_email(email_for_ban, is_banned=True)
        redis.set(name=email_for_ban, value=settings.auth.BAN_MESSAGE, ex=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        logger.info(f"Superuser {producer.email} banned {email_for_ban}")
        return {
            "detail": f"User {email_for_ban} successful banned"
        }

    async def unban_user_by_email(self, email_for_unban: EmailStr, producer: UserTokenPayloadSchema):
        producer = await self.__repository.find_user_by_email(producer.email)
        if not producer.is_superuser:
            raise user_is_not_super_exception
        # await self.__repository.unban_user_by_email(email_for_unban)
        await self.__repository.update_user_by_email(email_for_unban, is_banned=False)
        redis.delete(email_for_unban)
        logger.info(f"Superuser {producer.email} unbanned {email_for_unban}")
        return {
            "detail": f"User {email_for_unban} successful unbanned"
        }

    async def init_admin(self, email: EmailStr, password):
        await self.__repository.init_admin(email, password)
