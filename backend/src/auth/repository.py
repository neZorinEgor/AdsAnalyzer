import datetime
from typing import Optional

from pydantic import EmailStr

from src.auth.core import IAuthRepository
from src.auth.models import UserModel
from src.auth.schemas import RegisterUserSchema
from src.database import session_factory
from sqlalchemy import select, delete, update
from src.auth.utils import hash_password


class AuthRepository(IAuthRepository):
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
    async def delete_user_by_email(email: EmailStr) -> None:
        async with session_factory() as session:
            delete_statement = delete(UserModel).where(UserModel.email == email)
            await session.execute(delete_statement)
            await session.commit()

    @staticmethod
    async def update_user_by_email(email: EmailStr, **kwargs):
        async with session_factory() as session:
            update_statement = update(UserModel).where(UserModel.email == email).values(**kwargs)
            await session.execute(update_statement)
            await session.commit()

    @staticmethod
    async def init_admin(email: EmailStr, password: str):
        async with session_factory() as session:
            admin = UserModel(email=email, password=hash_password(password), is_superuser=True)
            admin_exist_query = select(UserModel).where(UserModel.email == email)
            admin_exist_query = await session.execute(admin_exist_query)
            admin_exist = admin_exist_query.scalar_one_or_none()
            if not admin_exist:
                session.add(admin)
                await session.commit()
