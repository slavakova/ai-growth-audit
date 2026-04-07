from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectRead
from app.schemas.run import RunCreate, RunRead
from app.services.project_service import ProjectService
from app.services.run_service import RunService
from app.tasks.pipeline import launch_pipeline

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    return ProjectService(db).create_project(payload)


@router.get("", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectRead]:
    return ProjectService(db).list_projects()


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    project = ProjectService(db).get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/{project_id}/analyze", response_model=RunRead, status_code=status.HTTP_202_ACCEPTED)
def analyze_project(project_id: int, payload: RunCreate, db: Session = Depends(get_db)) -> RunRead:
    project = ProjectService(db).get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    run = RunService(db).start_run(project, payload.goal)
    launch_pipeline(run.id)
    return run
