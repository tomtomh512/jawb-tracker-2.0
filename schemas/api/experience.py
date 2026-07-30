from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class ExperienceBase(BaseModel):
    title: str | None = None
    organization: str | None = None
    location: str | None = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current_job: bool | None = None
    bullet_points: list[str] | None = Field(default_factory=list)


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(ExperienceBase):
    pass


class ExperienceResponse(ExperienceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)