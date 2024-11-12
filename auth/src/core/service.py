import logging
import smtplib
from email.message import EmailMessage

from celery import Celery
from pydantic import EmailStr, constr

from src.core.abstract import ABCAuthRepository
from src.core.schema import RegisterUserSchema, LoginUserSchema, JWTTokenInfo
from src.core.utils import encode_jwt, check_password, decode_jwt
from src.core.exceptions import (
    UserAlreadyExistException,
    InvalidCredentialsException,
    UserIsBlockedException,
)
from src.settings import settings

logger = logging.getLogger("auth.service")
celery = Celery("notifications", broker=settings.rabbitmq_url)


class AuthService:
    def __init__(self, repository):
        # Dependency inversion, so as not to depend on implementation ;)
        self.__repository: ABCAuthRepository = repository()

    async def register(self, new_user: RegisterUserSchema):
        # 1. Check if the user already exists ✅
        exist_user = await self.__repository.find_user_by_emil(new_user.email)
        if exist_user:
            logger.error(f"Try register {new_user.email}, but already exist.")
            raise UserAlreadyExistException
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

    async def reset_password(self, token: str, new_password: constr(min_length=8)):
        print(decode_jwt(token))

    @staticmethod
    def forgot_password(email: EmailStr) -> None:
        email_token = encode_jwt(payload={"email": email}, expire_minutes=30)
        reset_email_by_token_link = f"http://{settings.APP_HOST}:{settings.APP_PORT}/reset_password?token={email_token}"
        email_subject = "Password Reset Request"
        content = f'To reset your password, please click the following <a href="{reset_email_by_token_link}">link</a>'

        # Передаем данные для создания письма в задачу, а не сам объект EmailMessage
        AuthService.__send_email.delay(email_subject, email, content)

    @staticmethod
    @celery.task
    def __send_email(email_subject: str, email_to: str, content: str) -> None:
        email = EmailMessage()
        email["Subject"] = email_subject
        email["To"] = email_to
        email["From"] = settings.SMTP_EMAIL_FROM
        email.set_content(f"{content}", subtype="html")

        # Отправка письма
        with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as server:
            server.login(user=settings.SMTP_EMAIL_FROM, password=settings.SMTP_PASSWORD)
            server.send_message(email)
