import datetime

from src.database import Base, str_128, str_50, str_255
from sqlalchemy.orm import mapped_column, Mapped


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str_50] = mapped_column(nullable=False, unique=True)
    password: Mapped[str_255] = mapped_column(nullable=False, unique=False, )
    register_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(datetime.UTC))
    is_banned: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
