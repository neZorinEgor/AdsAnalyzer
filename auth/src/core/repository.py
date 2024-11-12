import datetime
import logging
from typing import Optional

from pydantic import EmailStr, constr

from src.core.abstract import ABCAuthRepository
from src.core.model import UserModel
from src.core.schema import RegisterUserSchema
from src.database import session_factory
from sqlalchemy import select, delete, update
from src.core.utils import hash_password

logger = logging.getLogger("auth.repository")


class AuthRepositoryImpl(ABCAuthRepository):
    @staticmethod
    async def find_user_by_email(email: EmailStr) -> Optional[UserModel]:
        async with session_factory() as session:
            user_by_email_query = select(UserModel).where(UserModel.email == email)
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

    @staticmethod
    async def reset_password(email: EmailStr, new_password: constr(min_length=8)):
        async with session_factory() as session:
            update_password_statement = update(UserModel).where(UserModel.email == email).values(password=new_password)
            await session.execute(update_password_statement)
            await session.commit()
