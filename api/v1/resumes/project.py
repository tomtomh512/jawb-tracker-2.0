from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.api.project import ProjectResponse, ProjectUpdate, ProjectCreate
from database import get_db
from sqlalchemy.orm import Session

from services.resume_services import project_service

router = APIRouter(
    prefix="/resumes/{resume_id}/projects",
    tags=["projects"]
)


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return project_service.get_projects(db, resume_id)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
        resume_id: UUID,
        project_id: UUID,
        db: Session = Depends(get_db)
):
    return project_service.get_project(db, resume_id, project_id)


@router.post("/", response_model=ProjectResponse)
def create_project(
        resume_id: UUID,
        project: ProjectCreate,
        db: Session = Depends(get_db)
):
    return project_service.create_project(db, resume_id, project)


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
        resume_id: UUID,
        project_id: UUID,
        project_update: ProjectUpdate,
        db: Session = Depends(get_db)
):
    return project_service.update_project(db, resume_id, project_id, project_update)


@router.delete("/{project_id}", status_code=204)
def delete_project(
        resume_id: UUID,
        project_id: UUID,
        db: Session = Depends(get_db)
):
    project_service.delete_project(db, resume_id, project_id)
    return None