from uuid import uuid4

from database import Base
from sqlalchemy import Integer, Column, String, Date, DateTime, Float, ForeignKey, Boolean, func, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


class Resume(Base):
    __tablename__ = "Resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    resumeName = Column(String, index=True, unique=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    websites = Column(ARRAY(String), nullable=True)

    education = relationship(
        "Education",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    experience = relationship(
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

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Education(Base):
    __tablename__ = "Education"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    school = Column(String, nullable=True)
    degree = Column(String, nullable=True)
    field_of_study = Column(String, nullable=True)
    gpa = Column(Float, nullable=True)
    honors = Column(ARRAY(String), nullable=True)
    coursework = Column(ARRAY(String), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    resume = relationship(
        "Resume",
        back_populates="education"
    )


class Experience(Base):
    __tablename__ = "Experience"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    title = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    location = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    current_job = Column(Boolean, nullable=True)
    bullet_points = Column(ARRAY(String), nullable=True)

    resume = relationship(
        "Resume",
        back_populates="experience"
    )


class Project(Base):
    __tablename__ = "Projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    technologies = Column(ARRAY(String), nullable=True)
    links = Column(ARRAY(String), nullable=True)
    bullet_points = Column(ARRAY(String), nullable=True)

    resume = relationship(
        "Resume",
        back_populates="projects"
    )


class SkillCategory(Base):
    __tablename__ = "SkillCategories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    category = Column(String, nullable=True)
    skills = Column(ARRAY(String), nullable=True)

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
    authors = Column(ARRAY(String), nullable=True)
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

    id = Column(Integer, primary_key=True)
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

    id = Column(Integer, primary_key=True)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("Resumes.id"), nullable=False)

    title = Column(String, nullable=True)
    entries = Column(ARRAY(String), nullable=True)

    resume = relationship(
        "Resume",
        back_populates="custom_sections"
    )