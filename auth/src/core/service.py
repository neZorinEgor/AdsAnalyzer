import logging
import smtplib
from datetime import timedelta
from email.message import EmailMessage
from redis import Redis

from celery import Celery
from pydantic import EmailStr, constr

from src.core.abstract import ABCAuthRepository
from src.core.schema import RegisterUserSchema, LoginUserSchema, JWTTokenInfo, UserTokenPayloadSchema
from src.core import utils as jwt_utils
from src.core.exceptions import (
    UserAlreadyExistException,
    InvalidCredentialsException,
    UserIsBlockedException, UserIsNotSuperException,
)
from src.core.utils import create_access_token
from src.settings import settings

logger = logging.getLogger("auth.service")
celery = Celery("notifications", broker=settings.redis_url)
redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=0)


class AuthService:
    def __init__(self, repository):
        # Dependency inversion, so as not to depend on implementation ;)
        self.__repository: ABCAuthRepository = repository()

    async def register(self, new_user: RegisterUserSchema) -> int:
        """
        Register user at platform
        """
        # 1. Check if the user already exists
        exist_user = await self.__repository.find_user_by_email(new_user.email)
        if exist_user:
            logger.error(f"Try register {new_user.email}, but already exist.")
            raise UserAlreadyExistException
        # 2. Saving the user
        logger.info(f"Successful save new user {new_user.email}")
        new_user_id = await self.__repository.save_user(new_user)
        return new_user_id

    async def login(self, login_user: LoginUserSchema) -> JWTTokenInfo:
        """
        Validate user and return JWT-Refresh+Access token
        """
        # 1. Verify that the user exists and is submitting the required credentials
        user = await self.__repository.find_user_by_email(login_user.email)
        if not user or not jwt_utils.check_password(login_user.password, user.password.encode()):
            logger.error(f"Try login by invalid credentials: {login_user.email}.")
            raise InvalidCredentialsException
        # 2. Check if the user is banned
        if user.is_banned:
            raise UserIsBlockedException
        # 3. Issue access JWT token
        logger.info(f"{login_user.email} successful login.")
        access_token = jwt_utils.create_access_token(user)
        refresh_token = jwt_utils.create_refresh_token(user)
        return JWTTokenInfo(access_token=access_token, refresh_token=refresh_token)

    async def refresh_jwt(self, user_credentials: UserTokenPayloadSchema):
        """
        Generate access token by refresh from credentials
        """
        user = await self.__repository.find_user_by_id(user_credentials.sub)
        return JWTTokenInfo(access_token=create_access_token(user))

    async def delete_my_account(self, user_id: int) -> None:
        """
        Delete current user by token from db
        """
        logger.info(f"User by id: {user_id} delete account.")
        return await self.__repository.delete_user_by_id(user_id)

    async def reset_password(self, token: str, new_password: constr(min_length=8)) -> None:
        """
        Reset password by token
        """
        user_email = jwt_utils.decode_jwt(token).get("email")
        await self.__repository.reset_password_by_email(
            email=user_email,
            new_password=new_password
        )
        logger.info(f"User {user_email} change password")

    async def forgot_password(self, email: EmailStr) -> None:
        """
        Send email on exist user address
        """
        user = await self.__repository.find_user_by_email(email=email)
        if not user:
            # Do not inform the user if the account exists for security reasons.
            # Just advise them to check their registration or verify the entered data if the email is incorrect.
            pass
        email_token = jwt_utils.encode_jwt(payload={"email": email}, expire_timedelta=timedelta(minutes=30))
        email_subject = "Password Reset Request"
        # TODO: HTML message
        content = f'{email_token}'
        logger.info(f"Send email for reset password at {email}")
        AuthService.__send_email.delay(email_subject, email, content)

    @staticmethod
    @celery.task
    def __send_email(email_subject: str, email_to: str, content: str) -> None:
        """
        Create email template
        """
        email = EmailMessage()
        email["Subject"] = email_subject
        email["To"] = email_to
        email["From"] = settings.SMTP_EMAIL_FROM
        email.set_content(f"{content}", subtype="html")
        # Send email
        with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as server:
            server.login(user=settings.SMTP_EMAIL_FROM, password=settings.SMTP_PASSWORD)
            server.send_message(email)

    async def ban_user_by_email(self, user_email: EmailStr, superuser: UserTokenPayloadSchema):
        superuser = await self.__repository.find_user_by_id(superuser.sub)
        if not superuser.is_superuser:
            raise UserIsNotSuperException
        await self.__repository.ban_user_by_email(user_email)
        redis.set(name=user_email, value=settings.auth.BAN_MESSAGE, ex=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        logger.info(f"Superuser {superuser.email} banned {user_email}")
        return {
            "detail": f"User {user_email} successful banned"
        }

    async def unban_user_by_email(self, user_email: EmailStr, superuser: UserTokenPayloadSchema):
        superuser = await self.__repository.find_user_by_id(superuser.sub)
        if not superuser.is_superuser:
            raise UserIsNotSuperException
        await self.__repository.unban_user_by_email(user_email)
        redis.delete(user_email)
        logger.info(f"Superuser {superuser.email} unbanned {user_email}")
        return {
            "detail": f"User {user_email} successful unbanned"
        }
