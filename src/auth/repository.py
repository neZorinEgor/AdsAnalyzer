import datetime

from src.auth.contract import ABCAuthRepository
from src.auth.exceptions import UserByThisEmailAlreadyExistException, InvalidCredentialsException
from src.auth.model import UserModel
from src.auth.schema import RegisterUserSchema, LoginUserSchema, UserCredentialsSchema
from src.database import session_factory
from sqlalchemy import select
from src.auth.utils import hash_password, check_password


class AuthRepositoryImpl(ABCAuthRepository):
    async def register(self, register_user: RegisterUserSchema) -> int:
        """
        Save user credentials in database
        """
        async with session_factory() as session:
            # Checking if the user exists
            exist_user_query = select(UserModel).where(UserModel.email == register_user.email)
            exist_user = await session.execute(exist_user_query)
            exist_user = exist_user.scalar_one_or_none()
            if exist_user:
                raise UserByThisEmailAlreadyExistException
            # Saving the user
            user = UserModel(
                email=register_user.email,
                password=hash_password(register_user.password),
                register_at=datetime.datetime.now(datetime.UTC)
            )
            session.add(user)
            await session.commit()
            return user.id

    async def login(self, login_user: LoginUserSchema) -> UserCredentialsSchema:
        """
        Find user and compare this credentials
        """
        async with session_factory() as session:
            # Checking if the user exists
            exist_user_query = select(UserModel).where(UserModel.email == login_user.email)
            exist_user = await session.execute(exist_user_query)
            exist_user = exist_user.scalar_one_or_none()
            # Compare input password and saved password
            if not exist_user or not check_password(login_user.password, hash_password(login_user.password)):
                raise InvalidCredentialsException
            return UserCredentialsSchema(id=exist_user.id, email=exist_user.email)

