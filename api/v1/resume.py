from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from limiter import limiter
from schemas.api.resume import ResumeCreate, ResumeResponse, ResumeUpdate, ResumeTextCreate, ResumeSummaryResponse
from database import get_db
from sqlalchemy.orm import Session
from services import resume_service

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)


@router.get("/", response_model=list[ResumeSummaryResponse])
def get_resumes(
        skip: int = Query(0, ge=0),
        limit: int = Query(5, ge=1, le=50),
        db: Session = Depends(get_db)
):
    return resume_service.get_resumes(db, skip, limit)


@router.get("/main", response_model=ResumeSummaryResponse)
def get_main_resume(db: Session = Depends(get_db)):
    return resume_service.get_main_resume(db)


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
@limiter.limit("3/minute")
async def parse_resume_text(
        request: Request,
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