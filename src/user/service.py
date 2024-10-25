import datetime

from src.settings import settings
from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.user.exceptions import bad_user_credentials_exception, user_banned_exceptions, user_already_exist_exception
from src.user.model import UserModel
from src.user.schema import LoginUser
from src.user.utils import encode_jwt


class AuthService:
    def __init__(self, session):
        self.session = session

    async def login(self,user_credentials: LoginUser):
        get_user_by_credentials_query = select(UserModel).filter(
            (UserModel.username == user_credentials.username) & (UserModel.password == user_credentials.password)
        )
        user = await self.session.execute(get_user_by_credentials_query)
        user = user.scalar_one_or_none()
        if not user or user is None:
            raise bad_user_credentials_exception
        if user.is_banned:
            raise user_banned_exceptions
        token = encode_jwt({
            "username": user.username,
            "register_at": str(user.register_at),
            "email": user.email,
            "id": user.id,
            "is_banned": user.is_banned
        }, private_key=settings.jwt_private_key)
        return token

    async def register(self, create_user_schema):
        # Проверка, существует ли пользователь
        exist_user_query = select(UserModel).where(
            (UserModel.email == create_user_schema.email) or (UserModel.username == create_user_schema.username)
        )
        exist_user = await self.session.execute(exist_user_query)
        exist_user = exist_user.scalar_one_or_none()
        if exist_user:
            raise user_already_exist_exception
        # Сохранение пользователя
        user_model = UserModel()
        user_model.username = create_user_schema.username
        user_model.email = create_user_schema.email
        user_model.password = create_user_schema.password
        user_model.register_at = datetime.datetime.now(datetime.UTC)
        self.session.add(user_model)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        return user_model
