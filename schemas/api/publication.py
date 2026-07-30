from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date

class PublicationBase(BaseModel):
    title: str | None = None
    venue: str | None = None
    publisher: str | None = None
    date: Optional[date] = None
    url: str | None = None


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(PublicationBase):
    pass


class PublicationResponse(PublicationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)