from sqlalchemy.orm import Session

from app.services.crawler.site_crawler_service import SiteCrawlerService
from app.services.run_service import RunService


class PipelineService:
    """Scaffold service for future real integrations."""

    def __init__(self, db: Session):
        self.db = db
        self.run_service = RunService(db)

    def intake(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "intake", "note": "[MOCK] Intake complete"}

    def crawl(self, run_id: int) -> dict:
        run = self.run_service.get_run(run_id)
        if run is None:
            return {"run_id": run_id, "stage": "crawl", "error": "run not found"}

        crawler = SiteCrawlerService(self.db)
        page = crawler.crawl_run_primary_page(run)
        return {"run_id": run_id, "stage": "crawl", "saved_page_id": page.id if page else None}

    def page_understanding(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "page_understanding", "note": "[MOCK] Page understanding"}

    def query_builder(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "query_builder", "note": "[MOCK] Query list"}

    def serp_collection(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "serp_collection", "note": "[MOCK] SERP snapshots"}

    def competitor_selection(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "competitor_selection", "note": "[MOCK] Competitor selection"}

    def competitor_crawl(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "competitor_crawl", "note": "[MOCK] Competitor crawl"}

    def reputation_collection(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "reputation_collection", "note": "[MOCK] Reputation data"}

    def comparison(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "comparison", "note": "[MOCK] Comparison metrics"}

    def recommendations(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "recommendations", "note": "[MOCK] Recommendations"}

    def generation(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "generation", "note": "[MOCK] Generated assets"}

    def finalize(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": "finalize", "note": "[MOCK] Finalized"}
