from celery import chain

from app.db.session import SessionLocal
from app.models.enums import RunStatus
from app.services.pipeline_service import PipelineService
from app.services.run_service import RunService
from app.tasks.celery_app import celery_app


def _execute_stage(run_id: int, stage_name: str) -> None:
    db = SessionLocal()
    try:
        run_service = RunService(db)
        pipeline_service = PipelineService()
        run_service.set_stage(run_id, stage_name, RunStatus.RUNNING)
        getattr(pipeline_service, stage_name)(run_id)
    finally:
        db.close()


@celery_app.task(name="pipeline.intake")
def intake(run_id: int) -> int:
    _execute_stage(run_id, "intake")
    return run_id


@celery_app.task(name="pipeline.crawl")
def crawl(run_id: int) -> int:
    _execute_stage(run_id, "crawl")
    return run_id


@celery_app.task(name="pipeline.page_understanding")
def page_understanding(run_id: int) -> int:
    _execute_stage(run_id, "page_understanding")
    return run_id


@celery_app.task(name="pipeline.query_builder")
def query_builder(run_id: int) -> int:
    _execute_stage(run_id, "query_builder")
    return run_id


@celery_app.task(name="pipeline.serp_collection")
def serp_collection(run_id: int) -> int:
    _execute_stage(run_id, "serp_collection")
    return run_id


@celery_app.task(name="pipeline.competitor_selection")
def competitor_selection(run_id: int) -> int:
    _execute_stage(run_id, "competitor_selection")
    return run_id


@celery_app.task(name="pipeline.competitor_crawl")
def competitor_crawl(run_id: int) -> int:
    _execute_stage(run_id, "competitor_crawl")
    return run_id


@celery_app.task(name="pipeline.reputation_collection")
def reputation_collection(run_id: int) -> int:
    _execute_stage(run_id, "reputation_collection")
    return run_id


@celery_app.task(name="pipeline.comparison")
def comparison(run_id: int) -> int:
    _execute_stage(run_id, "comparison")
    return run_id


@celery_app.task(name="pipeline.recommendations")
def recommendations(run_id: int) -> int:
    _execute_stage(run_id, "recommendations")
    return run_id


@celery_app.task(name="pipeline.generation")
def generation(run_id: int) -> int:
    _execute_stage(run_id, "generation")
    return run_id


@celery_app.task(name="pipeline.finalize")
def finalize(run_id: int) -> int:
    db = SessionLocal()
    try:
        run_service = RunService(db)
        run_service.set_stage(run_id, "finalize", RunStatus.RUNNING)
        run_service.finalize_with_mock_data(run_id)
    finally:
        db.close()
    return run_id


def launch_pipeline(run_id: int) -> None:
    workflow = chain(
        intake.s(run_id),
        crawl.s(),
        page_understanding.s(),
        query_builder.s(),
        serp_collection.s(),
        competitor_selection.s(),
        competitor_crawl.s(),
        reputation_collection.s(),
        comparison.s(),
        recommendations.s(),
        generation.s(),
        finalize.s(),
    )
    workflow.apply_async()
