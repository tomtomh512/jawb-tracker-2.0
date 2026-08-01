from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Note(BaseModel):
    title: str | None = None
    content: str
    copy_to_clipboard: bool | None = False


class NoteCreate(Note):
    pass


class NoteUpdate(Note):
    pass


class NoteResponse(Note):
    id: UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)