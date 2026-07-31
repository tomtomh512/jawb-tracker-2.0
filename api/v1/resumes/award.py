from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.api.resume_schemas.award import AwardResponse, AwardUpdate, AwardCreate
from database import get_db
from sqlalchemy.orm import Session

from services.resume_services import award_service

router = APIRouter(
    prefix="/resumes/{resume_id}/awards",
    tags=["awards"]
)


@router.get("/", response_model=list[AwardResponse])
def get_awards(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return award_service.get_awards(db, resume_id)


@router.get("/{award_id}", response_model=AwardResponse)
def get_award(
        resume_id: UUID,
        award_id: UUID,
        db: Session = Depends(get_db)
):
    return award_service.get_award(db, resume_id, award_id)


@router.post("/", response_model=AwardResponse)
def create_award(
        resume_id: UUID,
        award: AwardCreate,
        db: Session = Depends(get_db)
):
    return award_service.create_award(db, resume_id, award)


@router.patch("/{award_id}", response_model=AwardResponse)
def update_award(
        resume_id: UUID,
        award_id: UUID,
        award_update: AwardUpdate,
        db: Session = Depends(get_db)
):
    return award_service.update_award(db, resume_id, award_id, award_update)


@router.delete("/{award_id}", status_code=204)
def delete_award(
        resume_id: UUID,
        award_id: UUID,
        db: Session = Depends(get_db)
):
    award_service.delete_award(db, resume_id, award_id)
    return None