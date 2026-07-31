from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import JobPosting
from schemas.api.job_posting import JobPostingUpdate, JobPostingCreate


def get_job_postings(db: Session) -> list[JobPosting]:
    return db.query(JobPosting).all()


def get_job_posting(
        db: Session,
        job_posting_id: UUID,
) -> JobPosting:
    job_posting = db.query(JobPosting).filter(JobPosting.id == job_posting_id).first()
    if job_posting is None:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return job_posting


def create_job_posting(
        db: Session,
        job_posting_create: JobPostingCreate,
) -> JobPosting:
    db_job_posting = JobPosting(**job_posting_create.model_dump())

    db.add(db_job_posting)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create job posting") from None

    db.refresh(db_job_posting)
    return db_job_posting


def update_job_posting(
        db: Session,
        job_posting_id: UUID,
        job_posting_update: JobPostingUpdate,
) -> JobPosting:
    db_job_posting = get_job_posting(db, job_posting_id)
    if db_job_posting is None:
        return None

    update_data = job_posting_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job_posting, field, value)

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update job posting") from None

    db.refresh(db_job_posting)
    return db_job_posting


def delete_job_posting(
        db: Session,
        job_posting_id: UUID,
) -> JobPosting:
    db_job_posting = get_job_posting(db, job_posting_id)

    try:
        db.delete(db_job_posting)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete job posting") from None

    return db_job_posting