from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.api.resume_schemas.certification import CertificationResponse, CertificationUpdate, CertificationCreate
from database import get_db
from sqlalchemy.orm import Session

from services.resume_services import certification_service

router = APIRouter(
    prefix="/resumes/{resume_id}/certifications",
    tags=["certifications"]
)


@router.get("/", response_model=list[CertificationResponse])
def get_certifications(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return certification_service.get_certifications(db, resume_id)


@router.get("/{certification_id}", response_model=CertificationResponse)
def get_certification(
        resume_id: UUID,
        certification_id: UUID,
        db: Session = Depends(get_db)
):
    return certification_service.get_certification(db, resume_id, certification_id)


@router.post("/", response_model=CertificationResponse)
def create_certification(
        resume_id: UUID,
        certification: CertificationCreate,
        db: Session = Depends(get_db)
):
    return certification_service.create_certification(db, resume_id, certification)


@router.patch("/{certification_id}", response_model=CertificationResponse)
def update_certification(
        resume_id: UUID,
        certification_id: UUID,
        certification_update: CertificationUpdate,
        db: Session = Depends(get_db)
):
    return certification_service.update_certification(db, resume_id, certification_id, certification_update)


@router.delete("/{certification_id}", status_code=204)
def delete_certification(
        resume_id: UUID,
        certification_id: UUID,
        db: Session = Depends(get_db)
):
    certification_service.delete_certification(db, resume_id, certification_id)
    return None