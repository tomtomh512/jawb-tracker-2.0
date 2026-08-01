from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import (
    Resume,
    Education,
    Experience,
    Project,
    SkillCategory,
    Certification,
    Publication,
    Award,
    CustomSection,
)
from schemas.api.resume import ResumeCreate, ResumeUpdate
from utils.resume_parser import parse_resume_from_text


def get_resumes(
        db: Session,
        skip: int = 0,
        limit: int = 5
) -> list[Resume]:
    return (
        db.query(Resume)
        .order_by(Resume.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_resume(
        db: Session,
        resume_id: UUID
) -> Resume:
    db_resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    return db_resume


def create_resume(
        db: Session,
        resume_create: ResumeCreate
) -> Resume:
    is_first_resume = db.query(Resume).first() is None

    db_resume = Resume(
        resume_name=resume_create.resume_name,
        is_main=is_first_resume,
        name=resume_create.name,
        email=resume_create.email,
        phone=resume_create.phone,
        location=resume_create.location,
        summary=resume_create.summary,
        websites=resume_create.websites,
        educations=[Education(**e.model_dump()) for e in resume_create.educations],
        experiences=[Experience(**e.model_dump()) for e in resume_create.experiences],
        projects=[Project(**p.model_dump()) for p in resume_create.projects],
        skill_categories=[SkillCategory(**s.model_dump()) for s in resume_create.skill_categories],
        certifications=[Certification(**c.model_dump()) for c in resume_create.certifications],
        publications=[Publication(**p.model_dump()) for p in resume_create.publications],
        awards=[Award(**a.model_dump()) for a in resume_create.awards],
        custom_sections=[CustomSection(**cs.model_dump()) for cs in resume_create.custom_sections],
    )

    try:
        db.add(db_resume)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create resume") from None

    db.refresh(db_resume)
    return db_resume


async def parse_resume_text(
        db: Session,
        resume_text_content: str,
        resume_name: str,
) -> Resume:
    existing = db.query(Resume).filter(Resume.resume_name == resume_name).first()
    if existing is not None:
        raise HTTPException(status_code=400, detail="Resume name already exists")

    is_first_resume = db.query(Resume).first() is None

    parsed_resume = await parse_resume_from_text(resume_text_content)

    db_resume = Resume(
        resume_name=resume_name,
        is_main=is_first_resume,
        name=parsed_resume.basics.name,
        email=parsed_resume.basics.email,
        phone=parsed_resume.basics.phone,
        location=parsed_resume.basics.location,
        summary=parsed_resume.basics.summary,
        websites=parsed_resume.basics.websites,
        educations=[Education(**e.model_dump()) for e in parsed_resume.educations],
        experiences=[Experience(**e.model_dump()) for e in parsed_resume.experiences],
        projects=[Project(**p.model_dump()) for p in parsed_resume.projects],
        skill_categories=[SkillCategory(**s.model_dump()) for s in parsed_resume.skill_categories],
        certifications=[Certification(**c.model_dump()) for c in parsed_resume.certifications],
        publications=[Publication(**p.model_dump()) for p in parsed_resume.publications],
        awards=[Award(**a.model_dump()) for a in parsed_resume.awards],
        custom_sections=[CustomSection(**cs.model_dump()) for cs in parsed_resume.custom_sections],
    )

    try:
        db.add(db_resume)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create resume") from None

    db.refresh(db_resume)
    return db_resume


async def parse_resume_from_pdf(
    db: Session,
    resume_name: str,
    pdf: UploadFile,
) -> Resume:
    return None


def update_resume(
        db: Session,
        resume_id: UUID,
        resume_update: ResumeUpdate
) -> Resume:
    db_resume = get_resume(db, resume_id)

    update_data = resume_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_resume, field, value)

    try:
        db_resume.updated_at = func.now()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update resume") from None

    db.refresh(db_resume)
    return db_resume


def set_main_resume(
        db: Session,
        resume_id: UUID
) -> Resume:
    db_resume = get_resume(db, resume_id)

    try:
        db_resume.updated_at = func.now()

        db.query(Resume).filter(
            Resume.id != resume_id,
            Resume.is_main.is_(True),
        ).update({"is_main": False}, synchronize_session=False)

        db_resume.is_main = True

        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not set main resume") from None

    db.refresh(db_resume)
    return db_resume


def delete_resume(
        db: Session,
        resume_id: UUID
) -> Resume:
    db_resume = get_resume(db, resume_id)

    try:
        db.delete(db_resume)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete resume") from None

    return db_resume