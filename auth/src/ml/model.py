from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class ClusterizationModel(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    endpoint_path: Mapped[str] = mapped_column(unique=True, nullable=False)
