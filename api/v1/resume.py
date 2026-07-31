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
        resume_create: ResumeCreate,
        db: Session = Depends(get_db)
):
    return resume_service.create_resume(db, resume_create)


@router.post("/parse", response_model=ResumeResponse)
async def parse_resume_text(
        resume_text_create: ResumeTextCreate,
        db: Session = Depends(get_db)
):
    return await resume_service.parse_resume_text(
        db,
        resume_text_create.content,
        resume_text_create.resume_name,
    )


# @router.post("/parsePdf")
# def parse_resume_from_pdf():
#     return resume_service.parse_resume_from_pdf()


@router.patch("/{resume_id}", response_model=ResumeResponse)
def update_resume(
        resume_id: UUID,
        resume_update: ResumeUpdate,
        db: Session = Depends(get_db)
):
    return resume_service.update_resume(db, resume_id, resume_update)


@router.patch("/{resume_id}/main", response_model=ResumeResponse)
def set_main_resume(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return resume_service.set_main_resume(db, resume_id)


@router.delete("/{resume_id}", status_code=204)
def delete_resume(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    resume_service.delete_resume(db, resume_id)
    return None