from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import CustomSection
from schemas.api.custom_section import CustomSectionUpdate, CustomSectionCreate
from services.resume_service import get_resume


def get_custom_sections(
        db: Session,
        resume_id: UUID,
) -> list[CustomSection]:
    return db.query(CustomSection).filter(CustomSection.resume_id == resume_id).all()


def get_custom_section(
    db: Session,
    resume_id: UUID,
    custom_section_id: UUID,
) -> CustomSection:
    db_custom_section = (
        db.query(CustomSection)
        .filter(
            CustomSection.id == custom_section_id,
            CustomSection.resume_id == resume_id,
        )
        .first()
    )

    if db_custom_section is None:
        raise HTTPException(status_code=404, detail="CustomSection not found")

    return db_custom_section


def create_custom_section(
        db: Session,
        resume_id: UUID,
        custom_section: CustomSectionCreate,
) -> CustomSection:
    db_resume = get_resume(db, resume_id)

    db_custom_section = CustomSection(resume_id=resume_id, **custom_section.model_dump())

    try:
        db.add(db_custom_section)
        db_resume.updated_at = func.now()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create custom_section") from None

    db.refresh(db_custom_section)
    return db_custom_section


def update_custom_section(
        db: Session,
        resume_id: UUID,
        custom_section_id: UUID,
        custom_section_update: CustomSectionUpdate,
) -> CustomSection:
    db_custom_section = get_custom_section(db, resume_id, custom_section_id)
    if db_custom_section is None:
        return None

    update_data = custom_section_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_custom_section, field, value)

    try:
        db_custom_section.resume.updated_at = func.now()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update custom_section") from None

    db.refresh(db_custom_section)
    return db_custom_section


def delete_custom_section(
    db: Session,
    resume_id: UUID,
    custom_section_id: UUID,
) -> CustomSection:
    db_custom_section = get_custom_section(db, resume_id, custom_section_id)

    try:
        db_custom_section.resume.updated_at = func.now()
        db.delete(db_custom_section)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete custom_section") from None

    return db_custom_section