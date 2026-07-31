from enum import Enum
from uuid import uuid4

from database import Base
from sqlalchemy import Integer, Column, String, DateTime, Boolean, func, UUID, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


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


class JobPosting(Base):
    __tablename__ = "JobPostings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    link = Column(String, nullable=True)
    status = Column(
        SQLEnum(
            JobApplicationStatus,
            name="job_application_status_enum",
            values_callable=lambda enum: [e.value for e in enum],
        ),
        nullable=False,
        default=JobApplicationStatus.APPLIED,
        server_default=JobApplicationStatus.APPLIED.value,
    )

    title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    employment_type = Column(SQLEnum(EmploymentType, name="employment_type_enum"), nullable=True)
    location_raw = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    remote = Column(Boolean, nullable=True)
    remote_days_per_week = Column(Integer, nullable=True)
    responsibilities = Column(ARRAY(String), nullable=True, default=list)
    requirements = Column(ARRAY(String), nullable=True, default=list)
    skills = Column(ARRAY(String), nullable=True, default=list)
    education_minimum = Column(SQLEnum(EducationLevel, name="education_level_enum"), nullable=True)
    education_preferred = Column(SQLEnum(EducationLevel, name="education_level_enum"), nullable=True)
    min_salary = Column(Integer, nullable=True)
    max_salary = Column(Integer, nullable=True)
    currency = Column(String, nullable=True)
    period = Column(String, nullable=True)
    bonus = Column(Boolean, nullable=True)
    equity = Column(Boolean, nullable=True)
    visa_sponsorship = Column(Boolean, nullable=True)
    clearance_required = Column(Boolean, nullable=True)
    cover_letter = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    rubric = relationship(
        "Rubric",
        back_populates="job_posting",
        uselist=False,
        cascade="all, delete-orphan",
    )