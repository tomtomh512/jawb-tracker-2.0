from uuid import uuid4

from database import Base
from sqlalchemy import Integer, Column, String, Date, DateTime, Float, ForeignKey, Boolean, func, UUID, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


class Resume(Base):
    __tablename__ = "Resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    resumeName = Column(String, nullable=False, index=True, unique=True)
    is_main = Column(Boolean, nullable=False, default=False, server_default="false")
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    websites = Column(ARRAY(String), nullable=True, default=list)

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    educations = relationship(
        "Education",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    experiences = relationship(
        "Experience",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    projects = relationship(
        "Project",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    skill_categories = relationship(
        "SkillCategory",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    certifications = relationship(
        "Certification",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    publications = relationship(
        "Publication",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    awards = relationship(
        "Award",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    custom_sections = relationship(
        "CustomSection",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    rubrics = relationship(
        "Rubric",
        back_populates="resume",
        cascade="all",
    )

    __table_args__ = (
        Index(
            "ix_resumes_only_one_main",
            "is_main",
            unique=True,
            postgresql_where=is_main.is_(True),
        ),
    )


class Education(Base):
    __tablename__ = "Educations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    school = Column(String, nullable=True)
    degree = Column(String, nullable=True)
    field_of_study = Column(String, nullable=True)
    gpa = Column(Float, nullable=True)
    honors = Column(ARRAY(String), nullable=True, default=list)
    coursework = Column(ARRAY(String), nullable=True, default=list)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    resume = relationship(
        "Resume",
        back_populates="educations"
    )


class Experience(Base):
    __tablename__ = "Experiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    title = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    location = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    current_job = Column(Boolean, nullable=True)
    bullet_points = Column(ARRAY(String), nullable=True, default=list)

    resume = relationship(
        "Resume",
        back_populates="experiences"
    )


class Project(Base):
    __tablename__ = "Projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    technologies = Column(ARRAY(String), nullable=True, default=list)
    links = Column(ARRAY(String), nullable=True, default=list)
    bullet_points = Column(ARRAY(String), nullable=True, default=list)

    resume = relationship(
        "Resume",
        back_populates="projects"
    )


class SkillCategory(Base):
    __tablename__ = "SkillCategories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    category = Column(String, nullable=True)
    skills = Column(ARRAY(String), nullable=True, default=list)

    resume = relationship(
        "Resume",
        back_populates="skill_categories"
    )


class Certification(Base):
    __tablename__ = "Certifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    name = Column(String, nullable=True)
    issuer = Column(String, nullable=True)
    issue_date = Column(Date, nullable=True)
    expiration_date = Column(Date, nullable=True)
    credential_id = Column(String, nullable=True)
    url = Column(String, nullable=True)

    resume = relationship(
        "Resume",
        back_populates="certifications"
    )


class Publication(Base):
    __tablename__ = "Publications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    title = Column(String, nullable=True)
    authors = Column(ARRAY(String), nullable=True, default=list)
    venue = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    publication_date = Column(Date, nullable=True)
    url = Column(String, nullable=True)

    resume = relationship(
        "Resume",
        back_populates="publications"
    )


class Award(Base):
    __tablename__ = "Awards"

    id = Column(UUID, primary_key=True)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    name = Column(String, nullable=True)
    issuer = Column(String, nullable=True)
    award_date = Column(Date, nullable=True)
    description = Column(String, nullable=True)

    resume = relationship(
        "Resume",
        back_populates="awards"
    )


class CustomSection(Base):
    __tablename__ = "CustomSections"

    id = Column(UUID, primary_key=True)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    title = Column(String, nullable=True)
    entries = Column(ARRAY(String), nullable=True, default=list)

    resume = relationship(
        "Resume",
        back_populates="custom_sections"
    )