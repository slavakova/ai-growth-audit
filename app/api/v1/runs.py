from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.enums import AssetType
from app.schemas.run import (
    ComparisonMetricRead,
    CompetitorRead,
    GeneratedAssetRead,
    RecommendationRead,
    RunRead,
)
from app.services.run_service import RunService

router = APIRouter(prefix="/api/runs", tags=["runs"])


@router.get("/{run_id}", response_model=RunRead)
def get_run(run_id: int, db: Session = Depends(get_db)) -> RunRead:
    run = RunService(db).get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.get("/{run_id}/competitors", response_model=list[CompetitorRead])
def list_competitors(run_id: int, db: Session = Depends(get_db)) -> list[CompetitorRead]:
    return RunService(db).list_competitors(run_id)


@router.get("/{run_id}/comparison", response_model=list[ComparisonMetricRead])
def list_comparison(run_id: int, db: Session = Depends(get_db)) -> list[ComparisonMetricRead]:
    return RunService(db).list_comparison(run_id)


@router.get("/{run_id}/recommendations", response_model=list[RecommendationRead])
def list_recommendations(run_id: int, db: Session = Depends(get_db)) -> list[RecommendationRead]:
    return RunService(db).list_recommendations(run_id)


@router.get("/{run_id}/assets/{asset_type}", response_model=list[GeneratedAssetRead])
def list_assets(run_id: int, asset_type: AssetType, db: Session = Depends(get_db)) -> list[GeneratedAssetRead]:
    return RunService(db).list_assets(run_id, asset_type)
