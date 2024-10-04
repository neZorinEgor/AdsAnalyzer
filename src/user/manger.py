from typing import Optional
from fastapi import Depends
from fastapi.requests import Request

from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, CookieTransport
from src.user.model import UserModel, get_user_db

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[UserModel, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserModel, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: UserModel, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


# Функция для получения менеджера пользователей
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# Настраиваем CookieTransport для отправки JWT в куки
cookie_transport = CookieTransport(cookie_name="jwt_token", cookie_max_age=3600)


# Стратегия JWT для создания токена
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


# Настраиваем бэкэнд аутентификации через куки
auth_backend_cookie = AuthenticationBackend(
    name="cookie-jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPIUsers с поддержкой аутентификации через куки
fastapi_users = FastAPIUsers[UserModel, int](
    get_user_manager,
    [auth_backend_cookie]  # Используем куки-бэкэнд
)

# Текущий активный пользователь
current_active_user = fastapi_users.current_user(active=True)
