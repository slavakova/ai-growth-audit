from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class ProjectCreate(BaseModel):
    name: str
    website_url: HttpUrl
    region: str
    priority_service: str


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    website_url: str
    region: str
    priority_service: str
    created_at: datetime
