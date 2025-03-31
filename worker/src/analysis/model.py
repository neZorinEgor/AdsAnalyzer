from src.database import Base, str_255
from sqlalchemy.orm import Mapped, mapped_column


class AdsReportModel(Base):
    __tablename__ = "ads_report"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_email: Mapped[str_255] = mapped_column(nullable=False)
    report_id: Mapped[int] = mapped_column(nullable=False)
    is_ready: Mapped[bool] = mapped_column(default=False)
    info: Mapped[str_255] = mapped_column(nullable=True, default=None)
    bad_segments: Mapped[str_255] = mapped_column(nullable=True, default=None)
    path_to_clustered_df: Mapped[str_255] = mapped_column(nullable=True, default=None)
    path_to_impact_df: Mapped[str_255] = mapped_column(nullable=True, default=None)
