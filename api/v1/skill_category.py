from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.api.skill_category import SkillCategoryResponse, SkillCategoryUpdate, SkillCategoryCreate
from database import get_db
from sqlalchemy.orm import Session

from services import skill_category_service

router = APIRouter(
    prefix="/resumes/{resume_id}/skill-categories",
    tags=["skill categories"]
)


@router.get("/", response_model=list[SkillCategoryResponse])
def get_skill_categories(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return skill_category_service.get_skill_categories(db, resume_id)


@router.get("/{skill_category_id}", response_model=SkillCategoryResponse)
def get_skill_category(
        resume_id: UUID,
        skill_category_id: UUID,
        db: Session = Depends(get_db)
):
    return skill_category_service.get_skill_category(db, resume_id, skill_category_id)


@router.post("/", response_model=SkillCategoryResponse)
def create_skill_category(
        resume_id: UUID,
        skill_category: SkillCategoryCreate,
        db: Session = Depends(get_db)
):
    return skill_category_service.create_skill_category(db, resume_id, skill_category)


@router.patch("/{skill_category_id}", response_model=SkillCategoryResponse)
def update_skill_category(
        resume_id: UUID,
        skill_category_id: UUID,
        skill_category_update: SkillCategoryUpdate,
        db: Session = Depends(get_db)
):
    return skill_category_service.update_skill_category(db, resume_id, skill_category_id, skill_category_update)


@router.delete("/{skill_category_id}", status_code=204)
def delete_skill_category(
        resume_id: UUID,
        skill_category_id: UUID,
        db: Session = Depends(get_db)
):
    skill_category_service.delete_skill_category(db, resume_id, skill_category_id)
    return None