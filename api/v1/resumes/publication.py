from uuid import UUID

from fastapi import APIRouter, Depends

from schemas.api.publication import PublicationResponse, PublicationUpdate, PublicationCreate
from database import get_db
from sqlalchemy.orm import Session

from services.resume_services import publication_service

router = APIRouter(
    prefix="/resumes/{resume_id}/publications",
    tags=["publications"]
)


@router.get("/", response_model=list[PublicationResponse])
def get_publications(
        resume_id: UUID,
        db: Session = Depends(get_db)
):
    return publication_service.get_publications(db, resume_id)


@router.get("/{publication_id}", response_model=PublicationResponse)
def get_publication(
        resume_id: UUID,
        publication_id: UUID,
        db: Session = Depends(get_db)
):
    return publication_service.get_publication(db, resume_id, publication_id)


@router.post("/", response_model=PublicationResponse)
def create_publication(
        resume_id: UUID,
        publication: PublicationCreate,
        db: Session = Depends(get_db)
):
    return publication_service.create_publication(db, resume_id, publication)


@router.patch("/{publication_id}", response_model=PublicationResponse)
def update_publication(
        resume_id: UUID,
        publication_id: UUID,
        publication_update: PublicationUpdate,
        db: Session = Depends(get_db)
):
    return publication_service.update_publication(db, resume_id, publication_id, publication_update)


@router.delete("/{publication_id}", status_code=204)
def delete_publication(
        resume_id: UUID,
        publication_id: UUID,
        db: Session = Depends(get_db)
):
    publication_service.delete_publication(db, resume_id, publication_id)
    return None