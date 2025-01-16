from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase,  registry
from sqlalchemy import String
from src.settings import settings
from typing import Annotated


engine = create_async_engine(
    url=settings.mysql_async_url,
    echo=False,
)


session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


str_50 = Annotated[str, 50]
str_128 = Annotated[str, 128]
str_255 = Annotated[str, 255]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_50: String(50),
            str_128: String(128),
            str_255: String(255)
        }
    )
