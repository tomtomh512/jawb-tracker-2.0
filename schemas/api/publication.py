from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from datetime import date

class PublicationBase(BaseModel):
    title: str | None = None
    venue: str | None = None
    publisher: str | None = None
    publication_date: Optional[date] = None
    url: str | None = None


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(PublicationBase):
    pass


class PublicationResponse(PublicationBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)