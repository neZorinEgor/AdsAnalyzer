from src.database import Base, str_255, str_128
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey


class ADSInfoModel(Base):
    __tablename__ = "asd_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    report_name: Mapped[str_255] = mapped_column(nullable=False)
