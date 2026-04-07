from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AnalysisGoal, RunStatus
from app.models.mixins import TimestampMixin


class AnalysisRun(Base, TimestampMixin):
    __tablename__ = "analysis_runs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    goal: Mapped[AnalysisGoal] = mapped_column(Enum(AnalysisGoal, name="analysis_goal_enum"), nullable=False)
    status: Mapped[RunStatus] = mapped_column(
        Enum(RunStatus, name="run_status_enum"), nullable=False, default=RunStatus.PENDING, index=True
    )
    current_stage: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    selected_page_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    project = relationship("Project", back_populates="runs")
    site_pages = relationship("SitePage", back_populates="run", cascade="all,delete-orphan")
    search_queries = relationship("SearchQuery", back_populates="run", cascade="all,delete-orphan")
    competitors = relationship("Competitor", back_populates="run", cascade="all,delete-orphan")
    reputation_snapshots = relationship("ReputationSnapshot", back_populates="run", cascade="all,delete-orphan")
    comparison_metrics = relationship("ComparisonMetric", back_populates="run", cascade="all,delete-orphan")
    recommendations = relationship("Recommendation", back_populates="run", cascade="all,delete-orphan")
    generated_assets = relationship("GeneratedAsset", back_populates="run", cascade="all,delete-orphan")
