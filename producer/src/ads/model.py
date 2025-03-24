import datetime

from src.database import Base, str_255, str_128
from sqlalchemy.orm import mapped_column, Mapped
# from sqlalchemy import ForeignKey


class ADSInfoModel(Base):
    __tablename__ = "asd_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    # owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    # report_name: Mapped[str_255] = mapped_column(nullable=False)
    uploaded_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.today())
    is_ready: Mapped[bool] = mapped_column(default=False, nullable=False)
    optimal_clusters: Mapped[int] = mapped_column(nullable=False)
    bad_company_segments: Mapped[str_255] = mapped_column(nullable=False)
    cluster_image_link: Mapped[str_255] = mapped_column(nullable=False)

