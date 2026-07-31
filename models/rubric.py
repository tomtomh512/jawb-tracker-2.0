from uuid import uuid4

from database import Base
from sqlalchemy import Integer, Column, String, Date, DateTime, Float, ForeignKey, Boolean, func, UUID, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


class Rubric(Base):
    __tablename__ = "Rubrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    resume_id = Column(
        UUID(as_uuid=True),
        ForeignKey("Resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_posting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("JobPostings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    overall_score = Column(Float)
    items = relationship(
        "RubricItem",
        back_populates="rubric",
        cascade="all, delete-orphan",
    )
    missing_required = Column(ARRAY(String), default=list)
    strengths = Column(ARRAY(String), default=list)
    weaknesses = Column(ARRAY(String), default=list)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    resume = relationship("Resume", back_populates="rubrics")
    job_posting = relationship("JobPosting", back_populates="rubrics")


class RubricItem(Base):
    __tablename__ = "RubricItems"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    rubric_id = Column(
        UUID(as_uuid=True),
        ForeignKey("Rubrics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    importance = Column(Integer, nullable=False)
    required = Column(Boolean, nullable=False)
    weight = Column(Float, nullable=False)

    score = Column(Float, nullable=False)
    weighted_score = Column(Float, nullable=False)

    reasoning = Column(String, nullable=False)

    evidence = Column(ARRAY(String), default=list)
    strengths = Column(ARRAY(String), default=list)
    weaknesses = Column(ARRAY(String), default=list)

    rubric = relationship("Rubric", back_populates="items")