from app.models.enums import PipelineStage


class PipelineService:
    """Scaffold service for future real integrations.

    TODO: connect real crawler, SERP source, and LLM generation providers.
    """

    def intake(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.INTAKE, "note": "[MOCK] Intake complete"}

    def crawl(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.CRAWL, "note": "[MOCK] Site crawl"}

    def page_understanding(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.PAGE_UNDERSTANDING, "note": "[MOCK] Page understanding"}

    def query_builder(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.QUERY_BUILDER, "note": "[MOCK] Query list"}

    def serp_collection(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.SERP_COLLECTION, "note": "[MOCK] SERP snapshots"}

    def competitor_selection(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.COMPETITOR_SELECTION, "note": "[MOCK] Competitor selection"}

    def competitor_crawl(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.COMPETITOR_CRAWL, "note": "[MOCK] Competitor crawl"}

    def reputation_collection(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.REPUTATION_COLLECTION, "note": "[MOCK] Reputation data"}

    def comparison(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.COMPARISON, "note": "[MOCK] Comparison metrics"}

    def recommendations(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.RECOMMENDATIONS, "note": "[MOCK] Recommendations"}

    def generation(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.GENERATION, "note": "[MOCK] Generated assets"}

    def finalize(self, run_id: int) -> dict:
        return {"run_id": run_id, "stage": PipelineStage.FINALIZE, "note": "[MOCK] Finalized"}
