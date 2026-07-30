from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from datetime import date


class AwardBase(BaseModel):
    name: str | None = None
    issuer: str | None = None
    award_date: Optional[date] = None
    description: str | None = None


class AwardCreate(AwardBase):
    pass


class AwardUpdate(AwardBase):
    pass


class AwardResponse(AwardBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)