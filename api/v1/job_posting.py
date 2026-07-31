from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.api.job_posting import (JobPostingResponse, JobPostingUpdate, JobPostingCreate, JobPostingStatusUpdate,
                                     ParseJobPostingCreate, JobPostingCoverLetterUpdate, JobPostingScoreUpdate)
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


@router.post("/parse", response_model=JobPostingResponse)
async def parse_job_posting(
        parse_job_posting_create: ParseJobPostingCreate,
        db: Session = Depends(get_db),
):
    return await job_posting_service.parse_job_posting(
        db,
        parse_job_posting_create.link,
        parse_job_posting_create.content,
        parse_job_posting_create.resume_id,
        parse_job_posting_create.include_cover_letter,
        parse_job_posting_create.include_score,
        parse_job_posting_create.cover_letter_prompt,
    )


@router.patch("/{job_posting_id}", response_model=JobPostingResponse)
def update_job_posting(
        job_posting_id: UUID,
        job_posting_update: JobPostingUpdate,
        db: Session = Depends(get_db),
):
    return job_posting_service.update_job_posting(db, job_posting_id, job_posting_update)


@router.patch("/{job_posting_id}/status", response_model=JobPostingResponse)
def update_job_posting_status(
        job_posting_id: UUID,
        job_posting_status_update: JobPostingStatusUpdate,
        db: Session = Depends(get_db),
):
    return job_posting_service.update_job_posting_status(db, job_posting_id, job_posting_status_update.status)


@router.patch("/{job_posting_id}/cover-letter", response_model=JobPostingResponse)
async def update_job_posting_cover_letter(
        job_posting_id: UUID,
        job_posting_cover_letter_update: JobPostingCoverLetterUpdate,
        db: Session = Depends(get_db),
):
    return await job_posting_service.update_job_posting_cover_letter(
        db,
        job_posting_id,
        job_posting_cover_letter_update.resume_id,
        job_posting_cover_letter_update.prompt,
    )


@router.patch("/{job_posting_id}/score", response_model=JobPostingResponse)
async def update_job_posting_score(
        job_posting_id: UUID,
        job_posting_score_update: JobPostingScoreUpdate,
        db: Session = Depends(get_db),
):
    return await job_posting_service.update_job_posting_score(
        db,
        job_posting_id,
        job_posting_score_update.resume_id
    )


@router.delete("/{job_posting_id}", status_code=204)
def delete_job_posting(
        job_posting_id: UUID,
        db: Session = Depends(get_db),
):
    job_posting_service.delete_job_posting(db, job_posting_id)
    return None