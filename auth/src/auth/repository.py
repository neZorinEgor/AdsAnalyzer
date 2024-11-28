import datetime
import logging
from typing import Optional

from pydantic import EmailStr, constr

from src.auth.core import IAuthRepository
from src.auth.models import UserModel
from src.auth.schemas import RegisterUserSchema
from src.database import session_factory
from sqlalchemy import select, delete, update
from src.auth.utils import hash_password

logger = logging.getLogger("auth.repository")


class AuthRepository(IAuthRepository):
    @staticmethod
    async def find_user_by_id(user_id: int) -> Optional[UserModel]:
        async with session_factory() as session:
            user_by_id_query = select(UserModel).where(UserModel.id == user_id)
            user = await session.execute(user_by_id_query)
            user = user.scalar_one_or_none()
            return user

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
    async def reset_password_by_email(email: EmailStr, new_password: constr(min_length=8)):
        async with session_factory() as session:
            update_password_statement = update(UserModel).where(UserModel.email == email).values(password=hash_password(new_password))
            await session.execute(update_password_statement)
            await session.commit()

    @staticmethod
    async def ban_user_by_email(email: EmailStr):
        async with session_factory() as session:
            ban_user_statement = update(UserModel).where(UserModel.email == email).values(is_banned=True)
            await session.execute(ban_user_statement)
            await session.commit()

    @staticmethod
    async def unban_user_by_email(email: EmailStr):
        async with session_factory() as session:
            ban_user_statement = update(UserModel).where(UserModel.email == email).values(is_banned=False)
            await session.execute(ban_user_statement)
            await session.commit()

    @staticmethod
    async def init_admin(email: EmailStr, password):
        async with session_factory() as session:
            admin = UserModel(email=email, password=hash_password(password), is_superuser=True)
            admin_exist_query = select(UserModel).where(UserModel.email == email)
            admin_exist_query = await session.execute(admin_exist_query)
            admin_exist_query = admin_exist_query.scalar_one_or_none()
            if not admin_exist_query:
                session.add(admin)
                await session.commit()
