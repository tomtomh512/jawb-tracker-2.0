from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.api.custom_section import CustomSectionResponse, CustomSectionUpdate, CustomSectionCreate
from database import get_db
from sqlalchemy.orm import Session

from services import custom_section_service

router = APIRouter(
    prefix="/resumes/{resume_id}/custom-sections",
    tags=["custom sections"]
)


@router.get("/", response_model=list[CustomSectionResponse])
def get_custom_sections(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return custom_section_service.get_custom_sections(db, resume_id)


@router.get("/{custom_section_id}", response_model=CustomSectionResponse)
def get_custom_section(
        resume_id: UUID,
        custom_section_id: UUID,
        db: Session = Depends(get_db)
):
    return custom_section_service.get_custom_section(db, resume_id, custom_section_id)


@router.post("/", response_model=CustomSectionResponse)
def create_custom_section(
        resume_id: UUID,
        custom_section: CustomSectionCreate,
        db: Session = Depends(get_db)
):
    return custom_section_service.create_custom_section(db, resume_id, custom_section)


@router.patch("/{custom_section_id}", response_model=CustomSectionResponse)
def update_custom_section(
        resume_id: UUID,
        custom_section_id: UUID,
        custom_section_update: CustomSectionUpdate,
        db: Session = Depends(get_db)
):
    return custom_section_service.update_custom_section(db, resume_id, custom_section_id, custom_section_update)


@router.delete("/{custom_section_id}", status_code=204)
def delete_custom_section(
        resume_id: UUID,
        custom_section_id: UUID,
        db: Session = Depends(get_db)
):
    custom_section_service.delete_custom_section(db, resume_id, custom_section_id)
    return None