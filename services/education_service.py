from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import Education
from schemas.api.education import EducationUpdate, EducationCreate
from services.resume_service import get_resume


def get_educations(
        db: Session,
        resume_id: UUID,
) -> list[Education]:
    return db.query(Education).filter(Education.resume_id == resume_id).all()


def get_education(
    db: Session,
    resume_id: UUID,
    education_id: UUID,
) -> Education:
    db_education = (
        db.query(Education)
        .filter(
            Education.id == education_id,
            Education.resume_id == resume_id,
        )
        .first()
    )

    if db_education is None:
        raise HTTPException(status_code=404, detail="Education not found")

    return db_education


def create_education(
        db: Session,
        resume_id: UUID,
        education: EducationCreate,
) -> Education:
    db_resume = get_resume(db, resume_id)

    db_education = Education(resume_id=resume_id, **education.model_dump())

    try:
        db.add(db_education)
        db_resume.updated_at = func.now()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create education") from None

    db.refresh(db_education)
    return db_education


def update_education(
        db: Session,
        resume_id: UUID,
        education_id: UUID,
        education_update: EducationUpdate,
) -> Education:
    db_education = get_education(db, resume_id, education_id)
    if db_education is None:
        return None

    update_data = education_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_education, field, value)

    try:
        db_education.resume.updated_at = func.now()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update education") from None

    db.refresh(db_education)
    return db_education


def delete_education(
    db: Session,
    resume_id: UUID,
    education_id: UUID,
) -> Education:
    db_education = get_education(db, resume_id, education_id)

    db_education.resume.updated_at = func.now()

    try:
        db_education.resume.updated_at = func.now()
        db.delete(db_education)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete education") from None

    return db_education