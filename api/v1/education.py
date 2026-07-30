from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.api.education import EducationResponse, EducationUpdate, EducationCreate
from database import get_db
from sqlalchemy.orm import Session

from services import education_service

router = APIRouter(
    prefix="/resumes/{resume_id}/education",
    tags=["education"]
)


@router.get("/", response_model=list[EducationResponse])
def get_all_education(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return education_service.get_all_education(db, resume_id)


@router.get("/{education_id}", response_model=EducationResponse)
def get_education(
        resume_id: UUID,
        education_id: UUID,
        db: Session = Depends(get_db)
):
    return education_service.get_education(db, resume_id, education_id)


@router.post("/", response_model=EducationResponse)
def create_education(
        resume_id: UUID,
        education: EducationCreate,
        db: Session = Depends(get_db)
):
    return education_service.create_education(db, resume_id, education)


@router.patch("/{education_id}", response_model=EducationResponse)
def update_education(
        resume_id: UUID,
        education_id: UUID,
        education_update: EducationUpdate,
        db: Session = Depends(get_db)
):
    return education_service.update_education(db, resume_id, education_id, education_update)


@router.delete("/{education_id}", status_code=204)
def delete_education(
        resume_id: UUID,
        education_id: UUID,
        db: Session = Depends(get_db)
):
    education_service.delete_education(db, resume_id, education_id)
    return None