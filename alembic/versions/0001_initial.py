"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    analysis_goal_enum = sa.Enum("seo_growth", "lead_generation", "conversion_rate", name="analysis_goal_enum")
    run_status_enum = sa.Enum("pending", "running", "completed", "failed", name="run_status_enum")
    asset_type_enum = sa.Enum("landing_page", "blog_post", "ad_copy", name="asset_type_enum")

    analysis_goal_enum.create(op.get_bind(), checkfirst=True)
    run_status_enum.create(op.get_bind(), checkfirst=True)
    asset_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("website_url", sa.String(length=2048), nullable=False),
        sa.Column("region", sa.String(length=128), nullable=False),
        sa.Column("priority_service", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_projects_id", "projects", ["id"])
    op.create_index("ix_projects_website_url", "projects", ["website_url"])
    op.create_index("ix_projects_region", "projects", ["region"])

    op.create_table(
        "analysis_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("goal", analysis_goal_enum, nullable=False),
        sa.Column("status", run_status_enum, nullable=False),
        sa.Column("current_stage", sa.String(length=64), nullable=True),
        sa.Column("error_message", sa.String(length=1024), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_analysis_runs_id", "analysis_runs", ["id"])
    op.create_index("ix_analysis_runs_project_id", "analysis_runs", ["project_id"])
    op.create_index("ix_analysis_runs_status", "analysis_runs", ["status"])

    table_defs = [
        (
            "site_pages",
            [
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("run_id", sa.Integer(), sa.ForeignKey("analysis_runs.id", ondelete="CASCADE"), nullable=False),
                sa.Column("url", sa.String(length=2048), nullable=False),
                sa.Column("title", sa.String(length=512), nullable=True),
                sa.Column("summary", sa.Text(), nullable=True),
                sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            ],
            [("ix_site_pages_run_id", ["run_id"])],
        ),
        (
            "search_queries",
            [
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("run_id", sa.Integer(), sa.ForeignKey("analysis_runs.id", ondelete="CASCADE"), nullable=False),
                sa.Column("query", sa.String(length=512), nullable=False),
                sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            ],
            [("ix_search_queries_run_id", ["run_id"]), ("ix_search_queries_query", ["query"])],
        ),
        (
            "search_results",
            [
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("search_query_id", sa.Integer(), sa.ForeignKey("search_queries.id", ondelete="CASCADE"), nullable=False),
                sa.Column("rank", sa.Integer(), nullable=False),
                sa.Column("title", sa.String(length=512), nullable=False),
                sa.Column("url", sa.String(length=2048), nullable=False),
                sa.Column("snippet", sa.String(length=1024), nullable=True),
                sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            ],
            [("ix_search_results_search_query_id", ["search_query_id"])],
        ),
        (
            "competitors",
            [
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("run_id", sa.Integer(), sa.ForeignKey("analysis_runs.id", ondelete="CASCADE"), nullable=False),
                sa.Column("domain", sa.String(length=255), nullable=False),
                sa.Column("reason", sa.String(length=512), nullable=True),
                sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            ],
            [("ix_competitors_run_id", ["run_id"]), ("ix_competitors_domain", ["domain"])],
        ),
        (
            "competitor_pages",
            [
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("competitor_id", sa.Integer(), sa.ForeignKey("competitors.id", ondelete="CASCADE"), nullable=False),
                sa.Column("url", sa.String(length=2048), nullable=False),
                sa.Column("summary", sa.Text(), nullable=True),
                sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            ],
            [("ix_competitor_pages_competitor_id", ["competitor_id"])],
        ),
        (
            "reputation_snapshots",
            [
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("run_id", sa.Integer(), sa.ForeignKey("analysis_runs.id", ondelete="CASCADE"), nullable=False),
                sa.Column("source", sa.String(length=128), nullable=False),
                sa.Column("rating", sa.Float(), nullable=True),
                sa.Column("volume", sa.Integer(), nullable=True),
                sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            ],
            [("ix_reputation_snapshots_run_id", ["run_id"])],
        ),
        (
            "comparison_metrics",
            [
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("run_id", sa.Integer(), sa.ForeignKey("analysis_runs.id", ondelete="CASCADE"), nullable=False),
                sa.Column("metric_name", sa.String(length=128), nullable=False),
                sa.Column("your_value", sa.String(length=256), nullable=True),
                sa.Column("competitor_avg", sa.String(length=256), nullable=True),
                sa.Column("delta", sa.String(length=256), nullable=True),
                sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            ],
            [("ix_comparison_metrics_run_id", ["run_id"])],
        ),
        (
            "recommendations",
            [
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("run_id", sa.Integer(), sa.ForeignKey("analysis_runs.id", ondelete="CASCADE"), nullable=False),
                sa.Column("title", sa.String(length=255), nullable=False),
                sa.Column("detail", sa.Text(), nullable=False),
                sa.Column("priority", sa.String(length=32), nullable=False),
                sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            ],
            [("ix_recommendations_run_id", ["run_id"]), ("ix_recommendations_priority", ["priority"])],
        ),
        (
            "generated_assets",
            [
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("run_id", sa.Integer(), sa.ForeignKey("analysis_runs.id", ondelete="CASCADE"), nullable=False),
                sa.Column("asset_type", asset_type_enum, nullable=False),
                sa.Column("title", sa.String(length=255), nullable=False),
                sa.Column("content", sa.Text(), nullable=False),
                sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
                sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            ],
            [("ix_generated_assets_run_id", ["run_id"]), ("ix_generated_assets_asset_type", ["asset_type"])],
        ),
    ]

    for table_name, columns, indexes in table_defs:
        op.create_table(table_name, *columns)
        for index_name, fields in indexes:
            op.create_index(index_name, table_name, fields)


def downgrade() -> None:
    for table_name in [
        "generated_assets",
        "recommendations",
        "comparison_metrics",
        "reputation_snapshots",
        "competitor_pages",
        "competitors",
        "search_results",
        "search_queries",
        "site_pages",
        "analysis_runs",
        "projects",
    ]:
        op.drop_table(table_name)

    sa.Enum(name="asset_type_enum").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="run_status_enum").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="analysis_goal_enum").drop(op.get_bind(), checkfirst=True)
