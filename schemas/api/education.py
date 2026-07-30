from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class EducationBase(BaseModel):
    school: str | None = None
    degree: str | None = None
    field_of_study: str | None = None
    gpa: float | None = None
    honors: list[str] = Field(default_factory=list)
    coursework: list[str] = Field(default_factory=list)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class EducationCreate(EducationBase):
    pass


class EducationUpdate(EducationBase):
    pass


class EducationResponse(EducationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)