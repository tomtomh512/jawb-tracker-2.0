from uuid import UUID

from fastapi import HTTPException
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
from schemas.api.resume import ResumeCreate, ResumeUpdate, ResumeTextCreate
from utils.resume_parser import parse_resume


def get_resumes(db: Session) -> list[Resume]:
    return db.query(Resume).all()


def get_resume(
        db: Session,
        resume_id: UUID
) -> Resume:
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


def create_resume(
        db: Session,
        resume: ResumeCreate
) -> Resume:
    db_resume = Resume(
        resumeName=resume.resumeName,
        name=resume.name,
        email=resume.email,
        phone=resume.phone,
        location=resume.location,
        summary=resume.summary,
        websites=resume.websites,
        education=[Education(**e.model_dump()) for e in resume.education],
        experience=[Experience(**e.model_dump()) for e in resume.experience],
        projects=[Project(**p.model_dump()) for p in resume.projects],
        skill_categories=[SkillCategory(**s.model_dump()) for s in resume.skill_categories],
        certifications=[Certification(**c.model_dump()) for c in resume.certifications],
        publications=[Publication(**p.model_dump()) for p in resume.publications],
        awards=[Award(**a.model_dump()) for a in resume.awards],
        custom_sections=[CustomSection(**cs.model_dump()) for cs in resume.custom_sections],
    )

    db.add(db_resume)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create resume") from None

    db.refresh(db_resume)
    return db_resume


async def create_resume_from_text(
        db: Session,
        resume_text: ResumeTextCreate
):
    test = await parse_resume(resume_text.content)
    return test



def create_resume_from_pdf():
    return "pdf"


def update_resume(
        db: Session,
        resume_id: UUID,
        resume_update: ResumeUpdate
) -> Resume:
    db_resume = get_resume(db, resume_id)
    if db_resume is None:
        return None

    update_data = resume_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_resume, field, value)

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update resume") from None

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