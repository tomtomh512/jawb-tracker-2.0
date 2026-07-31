from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.api.job_posting import JobPostingResponse, JobPostingUpdate, JobPostingCreate, \
    JobPostingStatusUpdate
from services import job_posting_service

router = APIRouter(
    prefix="/job-postings",
    tags=["job postings"]
)


@router.get("/", response_model=list[JobPostingResponse])
def get_job_postings(db: Session = Depends(get_db)):
    return job_posting_service.get_job_postings(db)


@router.get("/{job_posting_id}", response_model=JobPostingResponse)
def get_job_posting(
        job_posting_id: UUID,
        db: Session = Depends(get_db),
):
    return job_posting_service.get_job_posting(db, job_posting_id)


@router.post("/", response_model=JobPostingResponse)
def create_job_posting(
        job_posting_create: JobPostingCreate,
        db: Session = Depends(get_db),
):
    return job_posting_service.create_job_posting(db, job_posting_create)


@router.post("/parse")
def parse_job_posting():
    pass


@router.post("/{job_posting_id}/score")
def create_job_posting_score():
    pass


@router.post("/{job_posting_id}/cover-letter")
def create_job_posting_cover_letter():
    pass


@router.patch("/{job_posting_id}")
def update_job_posting(
        job_posting_id: UUID,
        job_posting_update: JobPostingUpdate,
        db: Session = Depends(get_db),
):
    return job_posting_service.update_job_posting(db, job_posting_id, job_posting_update)


@router.delete("/{job_posting_id}")
def delete_job_posting(
        job_posting_id: UUID,
        db: Session = Depends(get_db),
):
    job_posting_service.delete_job_posting(db, job_posting_id)
    return None


@router.patch("/{job_posting_id}/status")
def set_job_posting_status(
        job_posting_id: UUID,
        payload: JobPostingStatusUpdate,
        db: Session = Depends(get_db),
):
    return job_posting_service.set_job_posting_status(db, job_posting_id, payload)