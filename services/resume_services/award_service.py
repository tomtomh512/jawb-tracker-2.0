from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import Award
from schemas.api.resume_schemas.award import AwardUpdate, AwardCreate
from services.resume_services.resume_service import get_resume


def get_awards(
        db: Session,
        resume_id: UUID,
) -> list[Award]:
    return db.query(Award).filter(Award.resume_id == resume_id).all()


def get_award(
    db: Session,
    resume_id: UUID,
    award_id: UUID,
) -> Award:
    award = (
        db.query(Award)
        .filter(
            Award.id == award_id,
            Award.resume_id == resume_id,
        )
        .first()
    )

    if award is None:
        raise HTTPException(status_code=404, detail="Award not found")

    return award


def create_award(
        db: Session,
        resume_id: UUID,
        award: AwardCreate,
) -> Award:
    resume = get_resume(db, resume_id)

    db_award = Award(resume_id=resume_id, **award.model_dump())

    db.add(db_award)
    resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create award") from None

    db.refresh(db_award)
    return db_award


def update_award(
        db: Session,
        resume_id: UUID,
        award_id: UUID,
        award_update: AwardUpdate,
) -> Award:
    db_award = get_award(db, resume_id, award_id)
    if db_award is None:
        return None

    update_data = award_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_award, field, value)

    db_award.resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update award") from None

    db.refresh(db_award)
    return db_award


def delete_award(
    db: Session,
    resume_id: UUID,
    award_id: UUID,
) -> Award:
    db_award = get_award(db, resume_id, award_id)

    try:
        db.delete(db_award)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete award") from None

    return db_award