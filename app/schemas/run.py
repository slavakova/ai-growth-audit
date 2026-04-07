from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import AnalysisGoal, AssetType, RunStatus


class RunCreate(BaseModel):
    goal: AnalysisGoal


class RunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    goal: AnalysisGoal
    status: RunStatus
    current_stage: str | None
    error_message: str | None
    created_at: datetime


class CompetitorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    domain: str
    reason: str | None


class ComparisonMetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    metric_name: str
    your_value: str | None
    competitor_avg: str | None
    delta: str | None


class RecommendationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    detail: str
    priority: str


class GeneratedAssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_type: AssetType
    title: str
    content: str
