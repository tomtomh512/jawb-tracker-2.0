from uuid import UUID

from fastapi import APIRouter, Depends, Query

from database import get_db
from sqlalchemy.orm import Session

from schemas.api.note import NoteResponse, NoteCreate, NoteUpdate
from services import note_service

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@router.get("/", response_model=list[NoteResponse])
def get_notes(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db),
):
    return note_service.get_notes(db, skip, limit)


@router.get("/clipboard", response_model=list[NoteResponse])
def get_clipboard_notes(db: Session = Depends(get_db)):
    return note_service.get_clipboard_notes(db)


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
        note_id: UUID,
        db: Session = Depends(get_db)
):
    return note_service.get_note(db, note_id)

@router.post("/", response_model=NoteResponse)
def create_note(
        note_create: NoteCreate,
        db: Session = Depends(get_db)
):
    return note_service.create_note(db, note_create)

@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(
        note_id: UUID,
        note_update: NoteUpdate,
        db: Session = Depends(get_db),
):
    return note_service.update_note(db, note_id, note_update)

@router.delete("/{note_id}", status_code=204)
def delete_note(
        note_id: UUID,
        db: Session = Depends(get_db),
):
    note_service.delete_note(db, note_id)
    return None