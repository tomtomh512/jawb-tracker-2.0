from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models.resume import Publication
from schemas.api.publication import PublicationUpdate, PublicationCreate
from services.resume_service import get_resume


def get_publications(
        db: Session,
        resume_id: UUID,
) -> list[Publication]:
    return db.query(Publication).filter(Publication.resume_id == resume_id).all()


def get_publication(
    db: Session,
    resume_id: UUID,
    publication_id: UUID,
) -> Publication:
    db_publication = (
        db.query(Publication)
        .filter(
            Publication.id == publication_id,
            Publication.resume_id == resume_id,
        )
        .first()
    )

    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    return db_publication


def create_publication(
        db: Session,
        resume_id: UUID,
        publication: PublicationCreate,
) -> Publication:
    db_resume = get_resume(db, resume_id)

    db_publication = Publication(resume_id=resume_id, **publication.model_dump())

    try:
        db.add(db_publication)
        db_resume.updated_at = func.now()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create publication") from None

    db.refresh(db_publication)
    return db_publication


def update_publication(
        db: Session,
        resume_id: UUID,
        publication_id: UUID,
        publication_update: PublicationUpdate,
) -> Publication:
    db_publication = get_publication(db, resume_id, publication_id)

    update_data = publication_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_publication, field, value)

    try:
        db_publication.resume.updated_at = func.now()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update publication") from None

    db.refresh(db_publication)
    return db_publication


def delete_publication(
    db: Session,
    resume_id: UUID,
    publication_id: UUID,
) -> Publication:
    db_publication = get_publication(db, resume_id, publication_id)

    try:
        db_publication.resume.updated_at = func.now()
        db.delete(db_publication)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete publication") from None

    return db_publication