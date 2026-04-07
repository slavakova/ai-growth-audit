from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, payload: ProjectCreate) -> Project:
        project = Project(
            name=payload.name,
            website_url=str(payload.website_url),
            region=payload.region,
            priority_service=payload.priority_service,
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def list_projects(self) -> list[Project]:
        return list(self.db.scalars(select(Project).order_by(Project.id.desc())).all())

    def get_project(self, project_id: int) -> Project | None:
        return self.db.get(Project, project_id)
