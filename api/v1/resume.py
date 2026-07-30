from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from schemas.api.resume import ResumeCreate, ResumeResponse, ResumeUpdate
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
def create_resume_text():
    return "post resume text"


@router.post("/pdf")
def create_resume_pdf():
    return "post resume pdf"


@router.patch("/{resume_id}", response_model=ResumeResponse)
def update_resume(
        resume_id: UUID,
        resume_update: ResumeUpdate,
        db: Session = Depends(get_db)
):
    db_resume = resume_service.update_resume(db, resume_id, resume_update)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume


@router.delete("/{resume_id}", status_code=204)
def delete_resume(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    db_resume = resume_service.delete_resume(db, resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return None