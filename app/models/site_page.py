from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


class SitePage(Base, TimestampMixin):
    __tablename__ = "site_pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("analysis_runs.id", ondelete="CASCADE"), index=True)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    meta_description: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    h1: Mapped[str | None] = mapped_column(String(512), nullable=True)
    text_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    headings: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    cta_buttons: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    phones: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    forms_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    messengers: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    has_price: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_faq: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_reviews: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    page_type: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    extracted_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    run = relationship("AnalysisRun", back_populates="site_pages")
