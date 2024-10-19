import datetime

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import get_session
from src.user.model import UserModel
from src.user.schema import RegisterUser, LoginUser

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_credentials: LoginUser,
    session: AsyncSession = Depends(get_session),
):
    get_user_by_credentials_query = select(UserModel).filter(
        (UserModel.username == user_credentials.username) & (UserModel.password == user_credentials.password)
    )
    user = await session.execute(get_user_by_credentials_query)
    user = user.scalar_one_or_none()
    if not user or user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not founded, check username or password."
        )
    if user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is banned. Permission denied."
        )
    return user.__dict__


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
):
    pass


@router.post("/register", status_code=status.HTTP_200_OK)
async def register(
    create_user_schema: RegisterUser,
    session: AsyncSession = Depends(get_session),
):
    # Проверка, существует ли пользователь
    exist_user_query = select(UserModel).where(
        (UserModel.email == create_user_schema.email) or (UserModel.username == create_user_schema.username)
    )
    exist_user = await session.execute(exist_user_query)
    exist_user = exist_user.scalar_one_or_none()
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User by this email or username already exist"
        )
    # Сохранение пользователя
    user_model = UserModel()
    user_model.username = create_user_schema.username
    user_model.email = create_user_schema.email
    user_model.password = create_user_schema.password
    user_model.register_at = datetime.datetime.now(datetime.UTC)
    session.add(user_model)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {
        "msg": "Successful crate user",
        "user_id": user_model.id
    }


