from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RubricItemResponse(BaseModel):
    id: UUID
    name: str
    description: str
    importance: int
    required: bool
    weight: float
    score: float
    weighted_score: float
    reasoning: str
    evidence: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class RubricResponse(BaseModel):
    id: UUID
    resume_id: UUID
    resume_name: str
    job_posting_id: UUID

    job_title: str | None = None
    company: str | None = None
    overall_score: float
    items: list[RubricItemResponse] = Field(default_factory=list)
    missing_required: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)