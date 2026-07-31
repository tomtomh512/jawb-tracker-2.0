from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import JobPosting
from schemas.api.job_posting import JobPostingUpdate, JobPostingCreate, JobPostingStatusUpdate, \
    JobPostingCoverLetterCreate, JobPostingResponse, ParseJobPostingCreate
from schemas.api.resume_schemas.resume import ResumeResponse
from services.resume_services.resume_service import get_resume
from utils.cover_letter_generator import generate_cover_letter
from utils.job_posting_parser import parse_job_posting_from_text


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


async def parse_job_posting(
        db: Session,
        parse_job_posting_create: ParseJobPostingCreate,
) -> JobPosting:
    parsed_job_posting = await parse_job_posting_from_text(
        job_posting=parse_job_posting_create.content,
        llm_model="gemini"
    )

    db_job_posting = JobPosting(
        link=parse_job_posting_create.link,

        title=parsed_job_posting.title,
        company=parsed_job_posting.company,
        employment_type=parsed_job_posting.employment_type,

        location_raw=parsed_job_posting.location.raw if parsed_job_posting.location else None,
        city=parsed_job_posting.location.city if parsed_job_posting.location else None,
        state=parsed_job_posting.location.state if parsed_job_posting.location else None,
        country=parsed_job_posting.location.country if parsed_job_posting.location else None,
        remote=parsed_job_posting.location.remote if parsed_job_posting.location else None,
        remote_days_per_week=parsed_job_posting.location.remote_days_per_week if parsed_job_posting.location else None,

        responsibilities=parsed_job_posting.responsibilities,
        requirements=parsed_job_posting.requirements,
        skills=parsed_job_posting.skills,

        education_minimum=parsed_job_posting.education.minimum if parsed_job_posting.education else None,
        education_preferred=parsed_job_posting.education.preferred if parsed_job_posting.education else None,

        min_salary=parsed_job_posting.compensation.min_salary if parsed_job_posting.compensation else None,
        max_salary=parsed_job_posting.compensation.max_salary if parsed_job_posting.compensation else None,
        currency=parsed_job_posting.compensation.currency if parsed_job_posting.compensation else None,
        period=parsed_job_posting.compensation.period if parsed_job_posting.compensation else None,
        bonus=parsed_job_posting.compensation.bonus if parsed_job_posting.compensation else None,
        equity=parsed_job_posting.compensation.equity if parsed_job_posting.compensation else None,

        visa_sponsorship=parsed_job_posting.visa_sponsorship,
        clearance_required=parsed_job_posting.clearance_required,

        original=parse_job_posting_create.content,
    )

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


def set_job_posting_status(
        db: Session,
        job_posting_id: UUID,
        payload: JobPostingStatusUpdate
) -> JobPosting:
    db_job_posting = get_job_posting(db, job_posting_id)

    try:
        db_job_posting.status = payload.status
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not set status") from None

    db.refresh(db_job_posting)
    return db_job_posting


async def create_job_posting_cover_letter(
        db: Session,
        job_posting_id: UUID,
        payload: JobPostingCoverLetterCreate,
) -> JobPosting:
    db_resume = get_resume(db, payload.resume_id)
    db_job_posting = get_job_posting(db, job_posting_id)

    resume_text = ResumeResponse.model_validate(db_resume).model_dump_json(indent=2)
    job_posting_text = JobPostingResponse.model_validate(db_job_posting).model_dump_json(indent=2)

    if db_job_posting.original:
        job_posting_text = db_job_posting.original

    cover_letter = await generate_cover_letter(
        resume=resume_text,
        job_posting=job_posting_text,
        llm_model="gemini",
        custom_prompt=payload.prompt
    )

    try:
        db_job_posting.cover_letter = cover_letter.content
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not set cover letter") from None

    db.refresh(db_job_posting)
    return db_job_posting