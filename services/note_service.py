from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import Note
from schemas.api.note import NoteCreate, NoteUpdate


def get_notes(db: Session) -> list[Note]:
    return db.query(Note).all()

def get_note(
        db: Session,
        note_id: UUID
) -> Note:
    db_note = db.query(Note).filter(Note.id == note_id).first()

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return db_note

def create_note(
        db: Session,
        note_create: NoteCreate
) -> Note:
    db_note = Note(
        content=note_create.content,
        is_link=note_create.is_link,
        copy_to_clipboard=note_create.copy_to_clipboard
    )

    try:
        db.add(db_note)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create note") from None

    db.refresh(db_note)
    return db_note

def update_note(
        db: Session,
        note_id: UUID,
        note_update: NoteUpdate
) -> Note:
    db_note = get_note(db, note_id)

    update_data = note_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_note, field, value)

    try:
        db_note.updated_at = func.now()
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not update note") from None

    db.refresh(db_note)
    return db_note

def delete_note(
        db: Session,
        note_id: UUID
) -> Note:
    db_note = get_note(db, note_id)

    try:
        db.delete(db_note)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete note") from None

    return db_note