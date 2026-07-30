from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.api.resume import ResumeCreate, ResumeResponse, ResumeUpdate, ResumeTextCreate
from database import get_db
from sqlalchemy.orm import Session
from services import resume_service

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)


@router.get("/", response_model=list[ResumeResponse])
def get_resumes(db: Session = Depends(get_db)):
    return resume_service.get_resumes(db)


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return resume_service.get_resume(db, resume_id)


@router.post("/", response_model=ResumeResponse)
def create_resume(
        resume: ResumeCreate,
        db: Session = Depends(get_db)
):
    return resume_service.create_resume(db, resume)


@router.post("/text")
async def create_resume_from_text(
        resume_text: ResumeTextCreate,
        db: Session = Depends(get_db)
):
    return await resume_service.create_resume_from_text(db, resume_text)


@router.post("/pdf")
def create_resume_from_pdf():
    return resume_service.create_resume_from_pdf()


@router.patch("/{resume_id}", response_model=ResumeResponse)
def update_resume(
        resume_id: UUID,
        resume_update: ResumeUpdate,
        db: Session = Depends(get_db)
):
    return resume_service.update_resume(db, resume_id, resume_update)


@router.delete("/{resume_id}", status_code=204)
def delete_resume(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    resume_service.delete_resume(db, resume_id)
    return None