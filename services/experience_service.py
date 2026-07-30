from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import Experience
from schemas.api.experience import ExperienceUpdate, ExperienceCreate
from services.resume_service import get_resume


def get_all_experience(
        db: Session,
        resume_id: UUID,
) -> list[Experience]:
    return db.query(Experience).filter(Experience.resume_id == resume_id).all()


def get_experience(
    db: Session,
    resume_id: UUID,
    experience_id: UUID,
) -> Experience:
    experience = (
        db.query(Experience)
        .filter(
            Experience.id == experience_id,
            Experience.resume_id == resume_id,
        )
        .first()
    )

    if experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")

    return experience


def create_experience(
        db: Session,
        resume_id: UUID,
        experience: ExperienceCreate,
) -> Experience:
    resume = get_resume(db, resume_id)

    db_experience = Experience(resume_id=resume_id, **experience.model_dump())

    db.add(db_experience)
    resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create experience") from None

    db.refresh(db_experience)
    return db_experience


def update_experience(
        db: Session,
        resume_id: UUID,
        experience_id: UUID,
        experience_update: ExperienceUpdate,
) -> Experience:
    db_experience = get_experience(db, resume_id, experience_id)
    if db_experience is None:
        return None

    update_data = experience_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_experience, field, value)

    db_experience.resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update experience") from None

    db.refresh(db_experience)
    return db_experience


def delete_experience(
    db: Session,
    resume_id: UUID,
    experience_id: UUID,
) -> Experience:
    db_experience = get_experience(db, resume_id, experience_id)

    try:
        db.delete(db_experience)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete experience") from None

    return db_experience