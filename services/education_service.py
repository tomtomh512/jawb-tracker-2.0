from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import Education
from schemas.api.education import EducationUpdate, EducationCreate


def get_all_education(
        db: Session,
        resume_id: UUID,
) -> list[Education]:
    return db.query(Education).filter(Education.resume_id == resume_id).all()


def get_education(
    db: Session,
    resume_id: UUID,
    education_id: UUID,
) -> Education:
    education = (
        db.query(Education)
        .filter(
            Education.id == education_id,
            Education.resume_id == resume_id,
        )
        .first()
    )

    if education is None:
        raise HTTPException(status_code=404, detail="Education not found")

    return education


def create_education(
        db: Session,
        resume_id: UUID,
        education: EducationCreate,
) -> Education:
    pass


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

    db_education.resume.updated_at = func.now()

    try:
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

    try:
        db.delete(db_education)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete education") from None

    return db_education