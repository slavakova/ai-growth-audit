"""add crawler fields

Revision ID: 0002_crawler_fields
Revises: 0001_initial
Create Date: 2026-04-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_crawler_fields"
down_revision: str | None = "0001_initial"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("analysis_runs", sa.Column("selected_page_url", sa.String(length=2048), nullable=True))

    op.add_column("site_pages", sa.Column("meta_description", sa.String(length=1024), nullable=True))
    op.add_column("site_pages", sa.Column("h1", sa.String(length=512), nullable=True))
    op.add_column("site_pages", sa.Column("text_content", sa.Text(), nullable=True))
    op.add_column("site_pages", sa.Column("headings", sa.JSON(), nullable=False, server_default="[]"))
    op.add_column("site_pages", sa.Column("cta_buttons", sa.JSON(), nullable=False, server_default="[]"))
    op.add_column("site_pages", sa.Column("phones", sa.JSON(), nullable=False, server_default="[]"))
    op.add_column("site_pages", sa.Column("forms_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("site_pages", sa.Column("messengers", sa.JSON(), nullable=False, server_default="[]"))
    op.add_column("site_pages", sa.Column("has_price", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("site_pages", sa.Column("has_faq", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("site_pages", sa.Column("has_reviews", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("site_pages", sa.Column("page_type", sa.String(length=64), nullable=True))
    op.add_column("site_pages", sa.Column("extracted_json", sa.JSON(), nullable=False, server_default="{}"))
    op.create_index("ix_site_pages_page_type", "site_pages", ["page_type"])


def downgrade() -> None:
    op.drop_index("ix_site_pages_page_type", table_name="site_pages")
    op.drop_column("site_pages", "extracted_json")
    op.drop_column("site_pages", "page_type")
    op.drop_column("site_pages", "has_reviews")
    op.drop_column("site_pages", "has_faq")
    op.drop_column("site_pages", "has_price")
    op.drop_column("site_pages", "messengers")
    op.drop_column("site_pages", "forms_count")
    op.drop_column("site_pages", "phones")
    op.drop_column("site_pages", "cta_buttons")
    op.drop_column("site_pages", "headings")
    op.drop_column("site_pages", "text_content")
    op.drop_column("site_pages", "h1")
    op.drop_column("site_pages", "meta_description")

    op.drop_column("analysis_runs", "selected_page_url")
