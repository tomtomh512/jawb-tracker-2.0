from uuid import UUID

from fastapi import APIRouter, Depends
from schemas.api.resume import ResumeCreate, ResumeResponse
from database import get_db, engine, create_table, init_engine
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
def get_resume(resume_id: UUID, db: Session = Depends(get_db)):
    return resume_service.get_resume(db, resume_id)

@router.post("/")
def create_resume(
        resume: ResumeCreate,
        db: Session = Depends(get_db)
):
    return resume_service.create_resume(db, resume)

@router.post("/text")
def create_resume_text():
    return "post resume text"

@router.post("/pdf")
def create_resume_pdf():
    return "post resume pdf"

@router.patch("/{resume_id}")
def update_resume_pdf():
    return "patch resume"

@router.delete("/{resume_id}")
def delete_resume_pdf():
    return "delete resume"