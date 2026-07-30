from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import Certification
from schemas.api.certification import CertificationUpdate, CertificationCreate
from services.resume_services.resume_service import get_resume


def get_certifications(
        db: Session,
        resume_id: UUID,
) -> list[Certification]:
    return db.query(Certification).filter(Certification.resume_id == resume_id).all()


def get_certification(
    db: Session,
    resume_id: UUID,
    certification_id: UUID,
) -> Certification:
    certification = (
        db.query(Certification)
        .filter(
            Certification.id == certification_id,
            Certification.resume_id == resume_id,
        )
        .first()
    )

    if certification is None:
        raise HTTPException(status_code=404, detail="Certification not found")

    return certification


def create_certification(
        db: Session,
        resume_id: UUID,
        certification: CertificationCreate,
) -> Certification:
    resume = get_resume(db, resume_id)

    db_certification = Certification(resume_id=resume_id, **certification.model_dump())

    db.add(db_certification)
    resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create certification") from None

    db.refresh(db_certification)
    return db_certification


def update_certification(
        db: Session,
        resume_id: UUID,
        certification_id: UUID,
        certification_update: CertificationUpdate,
) -> Certification:
    db_certification = get_certification(db, resume_id, certification_id)
    if db_certification is None:
        return None

    update_data = certification_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_certification, field, value)

    db_certification.resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update certification") from None

    db.refresh(db_certification)
    return db_certification


def delete_certification(
    db: Session,
    resume_id: UUID,
    certification_id: UUID,
) -> Certification:
    db_certification = get_certification(db, resume_id, certification_id)

    try:
        db.delete(db_certification)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete certification") from None

    return db_certification