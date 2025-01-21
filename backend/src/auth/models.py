import datetime
from enum import StrEnum

from src.database import Base, str_255
from sqlalchemy.orm import mapped_column, Mapped


class Role(StrEnum):
    USER = "user"
    ADMIN = "admin"


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str_255] = mapped_column(nullable=False, unique=True)
    password: Mapped[str_255] = mapped_column(nullable=False, unique=False, )
    register_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(datetime.UTC))
    is_banned: Mapped[bool] = mapped_column(default=False, nullable=False)
    role: Mapped[Role] = mapped_column(default=Role.USER, nullable=False)
