from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.api.education import EducationResponse
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/resumes/{resume_id}/education",
    tags=["education"]
)

@router.get("/", response_model=list[EducationResponse])
def get_all_education(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    pass


@router.get("/{education_id}", response_model=EducationResponse)
def get_education(
        resume_id: UUID,
        education_id: UUID,
        db: Session = Depends(get_db)
):
    pass


@router.post("/", response_model=EducationResponse)
def create(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    pass


@router.get("/{education_id}", response_model=EducationResponse)
def update(
        resume_id: UUID,
        education_id: UUID,
        db: Session = Depends(get_db)
):
    pass


@router.get("/{education_id}", status_code=204)
def delete(
        resume_id: UUID,
        education_id: UUID,
        db: Session = Depends(get_db)
):
    pass