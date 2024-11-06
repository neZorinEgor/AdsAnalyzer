import datetime
import logging
from typing import Optional

from pydantic import EmailStr

from src.auth.abstract import ABCAuthRepository
from src.auth.model import UserModel
from src.auth.schema import RegisterUserSchema
from src.database import session_factory
from sqlalchemy import select, delete
from src.auth.utils import hash_password

logger = logging.getLogger("auth.repository")


class AuthRepositoryImpl(ABCAuthRepository):
    @staticmethod
    async def find_user_by_emil(user_email: EmailStr) -> Optional[UserModel]:
        async with session_factory() as session:
            user_by_email_query = select(UserModel).where(UserModel.email == user_email)
            user = await session.execute(user_by_email_query)
            user = user.scalar_one_or_none()
            return user

    @staticmethod
    async def save_user(user: RegisterUserSchema) -> int:
        async with session_factory() as session:
            user = UserModel(
                email=user.email,
                password=hash_password(user.password),
                register_at=datetime.datetime.now(datetime.UTC),
                is_banned=False,
                is_superuser=False,
            )
            session.add(user)
            await session.commit()
            return user.id

    @staticmethod
    async def delete_user_by_id(user_id: int):
        async with session_factory() as session:
            delete_statement = delete(UserModel).where(UserModel.id == user_id)
            await session.execute(delete_statement)
            await session.commit()
