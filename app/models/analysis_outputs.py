from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AssetType
from app.models.mixins import TimestampMixin


class ReputationSnapshot(Base, TimestampMixin):
    __tablename__ = "reputation_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("analysis_runs.id", ondelete="CASCADE"), index=True)
    source: Mapped[str] = mapped_column(String(128), nullable=False)
    rating: Mapped[float | None] = mapped_column(nullable=True)
    volume: Mapped[int | None] = mapped_column(nullable=True)

    run = relationship("AnalysisRun", back_populates="reputation_snapshots")


class ComparisonMetric(Base, TimestampMixin):
    __tablename__ = "comparison_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("analysis_runs.id", ondelete="CASCADE"), index=True)
    metric_name: Mapped[str] = mapped_column(String(128), nullable=False)
    your_value: Mapped[str | None] = mapped_column(String(256), nullable=True)
    competitor_avg: Mapped[str | None] = mapped_column(String(256), nullable=True)
    delta: Mapped[str | None] = mapped_column(String(256), nullable=True)

    run = relationship("AnalysisRun", back_populates="comparison_metrics")


class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("analysis_runs.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    detail: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    run = relationship("AnalysisRun", back_populates="recommendations")


class GeneratedAsset(Base, TimestampMixin):
    __tablename__ = "generated_assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("analysis_runs.id", ondelete="CASCADE"), index=True)
    asset_type: Mapped[AssetType] = mapped_column(Enum(AssetType, name="asset_type_enum"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    run = relationship("AnalysisRun", back_populates="generated_assets")
