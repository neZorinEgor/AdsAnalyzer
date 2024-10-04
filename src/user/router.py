from fastapi import Depends, APIRouter

from src.user.manger import fastapi_users, auth_backend_cookie, current_active_user
from src.user.model import UserModel
from src.user.schema import UserRead, UserUpdate, UserCreate

router = APIRouter(prefix="/auth")

# Маршрут для аутентификации с использованием куки
router.include_router(
    fastapi_users.get_auth_router(auth_backend_cookie), prefix="/jwt", tags=["auth"]
)

# Маршрут для регистрации
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)

# Маршрут для сброса пароля
router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)

# Маршрут для управления пользователями
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


# Пример защищенного маршрута с проверкой аутентификации
@router.get("/authenticated-route")
async def authenticated_route(user: UserModel = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
