from enum import StrEnum


class AnalysisGoal(StrEnum):
    SEO_GROWTH = "seo_growth"
    LEAD_GENERATION = "lead_generation"
    CONVERSION_RATE = "conversion_rate"


class RunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AssetType(StrEnum):
    LANDING_PAGE = "landing_page"
    BLOG_POST = "blog_post"
    AD_COPY = "ad_copy"


class PipelineStage(StrEnum):
    INTAKE = "intake"
    CRAWL = "crawl"
    PAGE_UNDERSTANDING = "page_understanding"
    QUERY_BUILDER = "query_builder"
    SERP_COLLECTION = "serp_collection"
    COMPETITOR_SELECTION = "competitor_selection"
    COMPETITOR_CRAWL = "competitor_crawl"
    REPUTATION_COLLECTION = "reputation_collection"
    COMPARISON = "comparison"
    RECOMMENDATIONS = "recommendations"
    GENERATION = "generation"
    FINALIZE = "finalize"
