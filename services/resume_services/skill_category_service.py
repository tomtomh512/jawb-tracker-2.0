from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import SkillCategory
from schemas.api.resume_schemas.skill_category import SkillCategoryUpdate, SkillCategoryCreate
from services.resume_services.resume_service import get_resume


def get_skill_categories(
        db: Session,
        resume_id: UUID,
) -> list[SkillCategory]:
    return db.query(SkillCategory).filter(SkillCategory.resume_id == resume_id).all()


def get_skill_category(
    db: Session,
    resume_id: UUID,
    skill_category_id: UUID,
) -> SkillCategory:
    skill_category = (
        db.query(SkillCategory)
        .filter(
            SkillCategory.id == skill_category_id,
            SkillCategory.resume_id == resume_id,
        )
        .first()
    )

    if skill_category is None:
        raise HTTPException(status_code=404, detail="SkillCategory not found")

    return skill_category


def create_skill_category(
        db: Session,
        resume_id: UUID,
        skill_category: SkillCategoryCreate,
) -> SkillCategory:
    resume = get_resume(db, resume_id)

    db_skill_category = SkillCategory(resume_id=resume_id, **skill_category.model_dump())

    db.add(db_skill_category)
    resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create skill_category") from None

    db.refresh(db_skill_category)
    return db_skill_category


def update_skill_category(
        db: Session,
        resume_id: UUID,
        skill_category_id: UUID,
        skill_category_update: SkillCategoryUpdate,
) -> SkillCategory:
    db_skill_category = get_skill_category(db, resume_id, skill_category_id)
    if db_skill_category is None:
        return None

    update_data = skill_category_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_skill_category, field, value)

    db_skill_category.resume.updated_at = func.now()

    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update skill_category") from None

    db.refresh(db_skill_category)
    return db_skill_category


def delete_skill_category(
    db: Session,
    resume_id: UUID,
    skill_category_id: UUID,
) -> SkillCategory:
    db_skill_category = get_skill_category(db, resume_id, skill_category_id)

    try:
        db.delete(db_skill_category)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete skill_category") from None

    return db_skill_category