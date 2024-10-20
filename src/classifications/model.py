import datetime
from src.database import Base, str_128
from sqlalchemy.orm import Mapped, mapped_column


class ClassificationHandlersModel(Base):
    __tablename__ = "handler"

    id: Mapped[int] = mapped_column(primary_key=True)
    endpoint_path: Mapped[str_128] = mapped_column(nullable=False)
    model_path: Mapped[str_128] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now(datetime.UTC))
