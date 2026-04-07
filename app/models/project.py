from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website_url: Mapped[str] = mapped_column(String(2048), nullable=False, index=True)
    region: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    priority_service: Mapped[str] = mapped_column(String(255), nullable=False)

    runs = relationship("AnalysisRun", back_populates="project", cascade="all,delete-orphan")
