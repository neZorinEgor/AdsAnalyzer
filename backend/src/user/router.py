from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession


from src.database import get_session
from src.user.dependancy import get_user_credentials_from_token
from src.user.schema import RegisterUser, LoginUser, UserReadInfo
from src.user.service import AuthService

router = APIRouter()


@router.post("/auth/login", status_code=status.HTTP_200_OK, tags=["Auth"])
async def login(
        response: Response,
        user_credentials: LoginUser,
        session: AsyncSession = Depends(get_session),
):
    token = await AuthService(session).login(user_credentials)
    response.set_cookie(key="TrainMeJWT", value=token, expires=3600)
    return {
        "msg": "Set JWT token."
    }


@router.post("/auth/logout", status_code=status.HTTP_200_OK, tags=["Auth"])
async def logout(
    response: Response
):
    response.delete_cookie("TrainMeJWT")
    return {
        "msg": "Goodbye!"
    }


@router.post("/auth/register", status_code=status.HTTP_200_OK, tags=["Auth"])
async def register(
        create_user_schema: RegisterUser,
        session: AsyncSession = Depends(get_session),
):
    user_model = await AuthService(session).register(create_user_schema)
    return {
        "msg": "Successful crate user",
        "user_id": user_model.id
    }


@router.get("/user/me", tags=["User"])
def get_current_user_credentials(user: UserReadInfo = Depends(get_user_credentials_from_token)):
    return user
