from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.api.resume_schemas.experience import ExperienceResponse, ExperienceUpdate, ExperienceCreate
from database import get_db
from sqlalchemy.orm import Session

from services.resume_services import experience_service

router = APIRouter(
    prefix="/resumes/{resume_id}/experiences",
    tags=["experiences"]
)


@router.get("/", response_model=list[ExperienceResponse])
def get_experiences(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return experience_service.get_experiences(db, resume_id)


@router.get("/{experience_id}", response_model=ExperienceResponse)
def get_experience(
        resume_id: UUID,
        experience_id: UUID,
        db: Session = Depends(get_db)
):
    return experience_service.get_experience(db, resume_id, experience_id)


@router.post("/", response_model=ExperienceResponse)
def create_experience(
        resume_id: UUID,
        experience: ExperienceCreate,
        db: Session = Depends(get_db)
):
    return experience_service.create_experience(db, resume_id, experience)


@router.patch("/{experience_id}", response_model=ExperienceResponse)
def update_experience(
        resume_id: UUID,
        experience_id: UUID,
        experience_update: ExperienceUpdate,
        db: Session = Depends(get_db)
):
    return experience_service.update_experience(db, resume_id, experience_id, experience_update)


@router.delete("/{experience_id}", status_code=204)
def delete_experience(
        resume_id: UUID,
        experience_id: UUID,
        db: Session = Depends(get_db)
):
    experience_service.delete_experience(db, resume_id, experience_id)
    return None