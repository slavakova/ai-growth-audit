from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class SearchQuery(Base, TimestampMixin):
    __tablename__ = "search_queries"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("analysis_runs.id", ondelete="CASCADE"), index=True)
    query: Mapped[str] = mapped_column(String(512), nullable=False, index=True)

    run = relationship("AnalysisRun", back_populates="search_queries")
    results = relationship("SearchResult", back_populates="search_query", cascade="all,delete-orphan")


class SearchResult(Base, TimestampMixin):
    __tablename__ = "search_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    search_query_id: Mapped[int] = mapped_column(ForeignKey("search_queries.id", ondelete="CASCADE"), index=True)
    rank: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    snippet: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    search_query = relationship("SearchQuery", back_populates="results")
