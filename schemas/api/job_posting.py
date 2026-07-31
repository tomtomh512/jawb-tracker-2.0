from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

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


class JobPostingUpdate(JobPosting):
    pass


class JobPostingStatusUpdate(BaseModel):
    status: JobApplicationStatus


class JobPostingCoverLetterCreate(BaseModel):
    resume_id: UUID
    prompt: str | None = None


class JobPostingResponse(JobPosting):
    id: UUID
    status: JobApplicationStatus
    rubric: RubricResponse | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CoverLetter(BaseModel):
    content: str


class ParseJobPostingCreate(BaseModel):
    link: str
    content: str


class JobPostingScoreCreate(BaseModel):
    resume_id: UUID