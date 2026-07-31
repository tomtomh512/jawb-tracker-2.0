from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import Project
from schemas.api.project import ProjectUpdate, ProjectCreate
from services.resume_service import get_resume


def get_projects(
        db: Session,
        resume_id: UUID,
) -> list[Project]:
    return db.query(Project).filter(Project.resume_id == resume_id).all()


def get_project(
    db: Session,
    resume_id: UUID,
    project_id: UUID,
) -> Project:
    db_project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.resume_id == resume_id,
        )
        .first()
    )

    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return db_project


def create_project(
        db: Session,
        resume_id: UUID,
        project: ProjectCreate,
) -> Project:
    db_resume = get_resume(db, resume_id)

    db_project = Project(resume_id=resume_id, **project.model_dump())

    db.add(db_project)
    db_resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create project") from None

    db.refresh(db_project)
    return db_project


def update_project(
        db: Session,
        resume_id: UUID,
        project_id: UUID,
        project_update: ProjectUpdate,
) -> Project:
    db_project = get_project(db, resume_id, project_id)
    if db_project is None:
        return None

    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)

    db_project.resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update project") from None

    db.refresh(db_project)
    return db_project


def delete_project(
    db: Session,
    resume_id: UUID,
    project_id: UUID,
) -> Project:
    db_project = get_project(db, resume_id, project_id)

    try:
        db.delete(db_project)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete project") from None

    return db_project