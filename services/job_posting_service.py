import asyncio
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, load_only

from models import JobPosting, Rubric, RubricItem, Resume
from schemas.api.job_posting import JobPostingUpdate, JobPostingCreate, JobPostingResponse, JobApplicationStatus
from schemas.api.resume import ResumeResponse
from services.resume_service import get_resume, parse_resume_text
from utils.cover_letter_generator import generate_cover_letter
from utils.job_posting_parser import parse_job_posting_from_text
from utils.score import score_resume


def get_job_postings(
        db: Session,
        status: JobApplicationStatus | None = None,
        skip: int = 0,
        limit: int = 50
) -> list[JobPosting]:
    db_job_posting = db.query(JobPosting)

    if status is not None:
        db_job_posting = db_job_posting.filter(JobPosting.status == status)

    return (
        db_job_posting
        .order_by(JobPosting.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_job_posting(
        db: Session,
        job_posting_id: UUID,
) -> JobPosting:
    db_job_posting = db.query(JobPosting).filter(JobPosting.id == job_posting_id).first()

    if db_job_posting is None:
        raise HTTPException(status_code=404, detail="Job posting not found")

    return db_job_posting


def create_job_posting(
        db: Session,
        job_posting_create: JobPostingCreate,
) -> JobPosting:
    db_job_posting = JobPosting(**job_posting_create.model_dump())

    try:
        db.add(db_job_posting)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create job posting") from None

    db.refresh(db_job_posting)
    return db_job_posting


async def parse_job_posting(
        db: Session,
        job_posting_content: str,
        job_posting_link: str | None = None,
        resume_id: UUID | None = None,
        custom_resume_content: str | None = None,
        include_cover_letter: bool = False,
        include_score: bool = False,
        cover_letter_prompt: str | None = None,
) -> JobPosting:
    if not job_posting_content.strip():
        raise HTTPException(status_code=400, detail="Job posting content is empty")

    if custom_resume_content is not None and not custom_resume_content.strip():
        raise HTTPException(status_code=400, detail="Custom resume content is empty")

    if (include_cover_letter or include_score) and not (resume_id or custom_resume_content):
        raise HTTPException(status_code=400, detail="A resume is required to generate a cover letter or score")

    parsed_job_posting = await parse_job_posting_from_text(
        job_posting=job_posting_content,
        llm_model="gemini"
    )

    db_job_posting = JobPosting(
        link=job_posting_link,

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

        original=job_posting_content,
    )

    try:
        db.add(db_job_posting)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create job posting") from None

    db.refresh(db_job_posting)

    if include_cover_letter or include_score:
        if resume_id:
            db_resume = get_resume(db, resume_id)

        elif custom_resume_content:
            company_part = db_job_posting.company or "job"
            resume_name = f"{company_part}_{db_job_posting.id}"

            existing = db.query(Resume).filter(Resume.resume_name == resume_name).first()

            if existing is not None:
                db.delete(existing)
                db.commit()

            db_resume = await parse_resume_text(
                db,
                custom_resume_content,
                resume_name,
            )

        resume_text = ResumeResponse.model_validate(db_resume).model_dump_json(indent=2)
        job_posting_text = JobPostingResponse.model_validate(db_job_posting).model_dump_json(indent=2)
        if db_job_posting.original:
            job_posting_text = db_job_posting.original

        tasks = {}
        if include_cover_letter:
            tasks["cover_letter"] = generate_cover_letter(
                resume=resume_text,
                job_posting=job_posting_text,
                llm_model="gemini",
                custom_prompt=cover_letter_prompt,
            )
        if include_score:
            tasks["score"] = score_resume(
                resume=resume_text,
                job_posting=job_posting_text,
                llm_model="gemini",
            )

        results = await asyncio.gather(*tasks.values())
        results_by_key = dict(zip(tasks.keys(), results))

        try:
            if "cover_letter" in results_by_key:
                db_job_posting.cover_letter = results_by_key["cover_letter"].content

            if "score" in results_by_key:
                scored_rubric = results_by_key["score"]
                db_job_posting.rubric = Rubric(
                    resume_id=db_resume.id,
                    resume_name=db_resume.resume_name,
                    job_posting_id=db_job_posting.id,
                    job_title=db_job_posting.title,
                    company=db_job_posting.company,
                    overall_score=scored_rubric.overall_score,
                    missing_required=scored_rubric.missing_required,
                    strengths=scored_rubric.strengths,
                    weaknesses=scored_rubric.weaknesses,
                    items=[
                        RubricItem(
                            name=item.name,
                            description=item.description,
                            importance=item.importance,
                            required=item.required,
                            weight=item.weight,
                            score=item.score,
                            weighted_score=item.weighted_score,
                            reasoning=item.reasoning,
                            evidence=item.evidence,
                            strengths=item.strengths,
                            weaknesses=item.weaknesses,
                        )
                        for item in scored_rubric.items
                    ],
                )

            db_job_posting.updated_at = func.now()
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Could not save generated content") from None

        db.refresh(db_job_posting)

    return db_job_posting


def update_job_posting(
        db: Session,
        job_posting_id: UUID,
        job_posting_update: JobPostingUpdate,
) -> JobPosting:
    db_job_posting = get_job_posting(db, job_posting_id)

    update_data = job_posting_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job_posting, field, value)

    try:
        db_job_posting.updated_at = func.now()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update job posting") from None

    db.refresh(db_job_posting)
    return db_job_posting


async def create_job_posting_cover_letter(
        db: Session,
        job_posting_id: UUID,
        resume_id: UUID | None = None,
        custom_resume_content: str | None = None,
        prompt: str | None = None,
) -> JobPosting:
    if not (resume_id or custom_resume_content):
        raise HTTPException(status_code=400, detail="A resume is required") from None

    db_job_posting = get_job_posting(db, job_posting_id)

    if resume_id:
        db_resume = get_resume(db, resume_id)

    elif custom_resume_content:
        company_part = db_job_posting.company or "job"
        resume_name = f"{company_part}_{db_job_posting.id}"

        existing = db.query(Resume).filter(Resume.resume_name == resume_name).first()

        if existing is not None:
            db.delete(existing)
            db.commit()

        db_resume = await parse_resume_text(
            db,
            custom_resume_content,
            resume_name,
        )

    resume_text = ResumeResponse.model_validate(db_resume).model_dump_json(indent=2)
    job_posting_text = JobPostingResponse.model_validate(db_job_posting).model_dump_json(indent=2)

    if db_job_posting.original:
        job_posting_text = db_job_posting.original

    cover_letter = await generate_cover_letter(
        resume=resume_text,
        job_posting=job_posting_text,
        llm_model="gemini",
        custom_prompt=prompt
    )

    try:
        db_job_posting.updated_at = func.now()
        db_job_posting.cover_letter = cover_letter.content
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not set cover letter") from None

    db.refresh(db_job_posting)
    return db_job_posting


def update_job_posting_cover_letter(
        db: Session,
        job_posting_id: UUID,
        content: str
):
    if not content.strip():
        raise HTTPException(status_code=400, detail="Cover letter content is empty") from None

    db_job_posting = get_job_posting(db, job_posting_id)

    try:
        db_job_posting.updated_at = func.now()
        db_job_posting.cover_letter = content
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not set cover letter") from None

    db.refresh(db_job_posting)
    return db_job_posting


async def create_job_posting_score(
        db: Session,
        job_posting_id: UUID,
        resume_id: UUID | None = None,
        custom_resume_content: str | None = None,
) -> JobPosting:
    if not (resume_id or custom_resume_content):
        raise HTTPException(status_code=400, detail="A resume is required") from None

    db_job_posting = get_job_posting(db, job_posting_id)

    if resume_id:
        db_resume = get_resume(db, resume_id)

    elif custom_resume_content:
        company_part = db_job_posting.company or "job"
        resume_name = f"{company_part}_{db_job_posting.id}"

        existing = db.query(Resume).filter(Resume.resume_name == resume_name).first()

        if existing is not None:
            db.delete(existing)
            db.commit()

        db_resume = await parse_resume_text(
            db,
            custom_resume_content,
            resume_name,
        )

    resume_text = ResumeResponse.model_validate(db_resume).model_dump_json(indent=2)
    job_posting_text = JobPostingResponse.model_validate(db_job_posting).model_dump_json(indent=2)

    if db_job_posting.original:
        job_posting_text = db_job_posting.original

    scored_rubric = await score_resume(
        resume=resume_text,
        job_posting=job_posting_text,
        llm_model="gemini"
    )

    db_rubric = Rubric(
        resume_id=resume_id,
        resume_name=db_resume.resume_name,
        job_posting_id=job_posting_id,
        job_title=db_job_posting.title,
        company=db_job_posting.company,
        overall_score=scored_rubric.overall_score,
        missing_required=scored_rubric.missing_required,
        strengths=scored_rubric.strengths,
        weaknesses=scored_rubric.weaknesses,
        items=[
            RubricItem(
                name=item.name,
                description=item.description,
                importance=item.importance,
                required=item.required,
                weight=item.weight,
                score=item.score,
                weighted_score=item.weighted_score,
                reasoning=item.reasoning,
                evidence=item.evidence,
                strengths=item.strengths,
                weaknesses=item.weaknesses,
            )
            for item in scored_rubric.items
        ],
    )

    try:
        if db_job_posting.rubric is not None:
            db.delete(db_job_posting.rubric)
            db.flush()

        db_job_posting.updated_at = func.now()
        db_job_posting.rubric = db_rubric

        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not set rubric") from None

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
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete job posting") from None

    return db_job_posting