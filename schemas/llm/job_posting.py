from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


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

class Location(BaseModel):
    raw: Optional[str] = Field(None, description="Original location text from the job posting")
    city: Optional[str] = Field(None, description="City where the job is located")
    state: Optional[str] = Field(None, description="State, province, or region where the job is located")
    country: Optional[str] = Field(None, description="Country where the job is located")
    remote: Optional[bool] = Field(None, description="Whether the position allows remote work")
    remote_days_per_week: Optional[int] = Field(None, description="Number of remote workdays per week, if specified")

class Education(BaseModel):
    minimum: Optional[EducationLevel] = Field(None, description="Minimum education level required")
    preferred: Optional[EducationLevel] = Field(None, description="Preferred education level")

class Compensation(BaseModel):
    min_salary: Optional[int] = Field(None, description="Minimum annual salary")
    max_salary: Optional[int] = Field(None, description="Maximum annual salary")
    currency: Optional[str] = Field(None, description="Currency used for the salary")
    period: Optional[str] = Field(None, description="Compensation period, such as yearly or hourly")
    bonus: Optional[bool] = Field(None, description="Whether the role includes bonus compensation")
    equity: Optional[bool] = Field(None, description="Whether the role includes equity compensation")

class ParsedJobPosting(BaseModel):
    title: Optional[str] = Field(None, description="Job title")
    company: Optional[str] = Field(None, description="Company offering the position")
    location: Optional[Location] = Field(None, description="Location details for the position")
    employment_type: Optional[EmploymentType] = Field(None, description="Employment type for the position")
    responsibilities: List[str] = Field(default_factory=list, description="Responsibilities associated with the position")
    requirements: List[str] = Field(default_factory=list, description="Requirements listed in the job posting")
    skills: List[str] = Field(default_factory=list, description="Skills mentioned in the job posting")
    education: Optional[Education] = Field(None, description="Education requirements for the position")
    compensation: Optional[Compensation] = Field(None, description="Compensation details for the position")
    visa_sponsorship: Optional[bool] = Field(None, description="Whether visa sponsorship is available")
    clearance_required: Optional[bool] = Field(None, description="Whether a security clearance is required")

class CoverLetter(BaseModel):
    content: Optional[str]