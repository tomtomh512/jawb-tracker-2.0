from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from schemas.api.rubric import RubricResponse


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "internship"
    FREELANCE = "freelance"


class EducationLevel(str, Enum):
    HIGH_SCHOOL = "high_school"
    ASSOCIATES = "associates"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    PHD = "phd"


class JobApplicationStatus(str, Enum):
    SAVED = "saved"
    APPLIED = "applied"
    ASSESSMENT = "assessment"
    INTERVIEW = "interview"
    OFFER = "offer"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    GHOSTED = "ghosted"


class JobPosting(BaseModel):
    link: str | None = None
    title: str | None = None
    company: str | None = None
    employment_type: EmploymentType | None = None
    location_raw: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    remote: bool | None = None
    remote_days_per_week: int | None = None
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    education_minimum: EducationLevel | None = None
    education_preferred: EducationLevel | None = None
    min_salary: int | None = None
    max_salary: int | None = None
    currency: str | None = None
    period: str | None = None
    bonus: bool | None = None
    equity: bool | None = None
    visa_sponsorship: bool | None = None
    clearance_required: bool | None = None
    original: str | None = None
    notes: str | None = None
    cover_letter: str | None = None


class JobPostingCreate(JobPosting):
    pass


class ParseJobPostingCreate(BaseModel):
    link: str | None = None
    content: str
    resume_id: UUID | None = None
    include_cover_letter: bool = False
    include_score: bool = False
    cover_letter_prompt: str | None = None


class JobPostingUpdate(JobPosting):
    status: JobApplicationStatus


class JobPostingCoverLetterCreate(BaseModel):
    resume_id: UUID
    prompt: str | None = None


class JobPostingCoverLetterUpdate(BaseModel):
    content: str = None


class JobPostingScoreCreate(BaseModel):
    resume_id: UUID


class JobPostingResponse(JobPosting):
    id: UUID
    status: JobApplicationStatus
    rubric: RubricResponse | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CoverLetter(BaseModel):
    content: str


class JobPostingSummaryResponse(BaseModel):
    id: UUID
    title: str | None = None
    company: str | None = None
    location_raw: str | None = None
    min_salary: int | None = None
    max_salary: int | None = None
    currency: str | None = None
    period: str | None = None
    created_at: datetime
    status: JobApplicationStatus
    overall_score: float | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def flatten_rubric_score(cls, obj):
        if isinstance(obj, dict):
            return obj
        return {
            "id": obj.id,
            "title": obj.title,
            "company": obj.company,
            "location_raw": obj.location_raw,
            "min_salary": obj.min_salary,
            "max_salary": obj.max_salary,
            "currency": obj.currency,
            "period": obj.period,
            "created_at": obj.created_at,
            "status": obj.status,
            "overall_score": obj.rubric.overall_score if obj.rubric else None,
        }