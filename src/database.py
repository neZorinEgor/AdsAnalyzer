from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.config import settings


# Async engin connector
engine = create_async_engine(
    url=settings.mysql_async_url,
    echo=True,
)

# Factory pattern
session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# Global database connector dependency
# Sample: session: AsyncSession = Depends(get_session)
async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session


class Base(DeclarativeBase):
    ...
