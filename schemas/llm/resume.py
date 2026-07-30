from enum import Enum
from typing import List, Optional
from datetime import date

from pydantic import BaseModel, Field


class Basics(BaseModel):
    name: Optional[str] = Field(None, description="Candidate's full name")
    email: Optional[str] = Field(None, description="Primary email address")
    phone: Optional[str] = Field(None, description="Primary phone number")
    location: Optional[str] = Field(None, description="City, state, province, or country listed on the resume")
    summary: Optional[str] = Field(None, description="Professional summary, objective, or profile statement")
    websites: List[str] = Field(default_factory=list, description="Personal websites and profile URLs such as GitHub, LinkedIn, or portfolio")

class Classification(str, Enum):
    EDUCATION = "education"
    EXPERIENCE = "experience"
    PROJECT = "project"
    SKILL_CATEGORY = "skill_category"
    CERTIFICATION = "certification"
    PUBLICATION = "publication"
    AWARD = "award"
    CUSTOM_SECTION = "custom_section"

class ResumeSection(BaseModel):
    name: Optional[str] = Field(None, description="The title or heading of the resume section (e.g., 'Education', 'Work Experience')")
    classification: Optional[Classification] = Field(None, description="The standardized classification of this section")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score from 0.0 to 1.0 that the classification is correct")
    content: List[str] = Field(default_factory=list, description="A list where each element is the raw text for a single entry in the section (e.g., one job, one project, one degree, one certification)")

class InitialResumeScanOutput(BaseModel):
    basics: Optional[Basics] = None
    resume_sections: List[ResumeSection] = Field(default_factory=list)

class Education(BaseModel):
    school: Optional[str] = Field(None, description="Name of the educational institution")
    degree: Optional[str] = Field(None, description="Degree earned or pursued, such as Bachelor of Science or Master of Arts")
    field_of_study: Optional[str] = Field(None, description="Major, concentration, or field of study")
    gpa: Optional[float] = Field(None, ge=0, le=5.0, description="Grade Point Average. Leave null if not explicitly mentioned")
    honors: List[str] = Field(default_factory=list, description="Academic honors or distinctions such as Dean's List or Magna Cum Laude")
    coursework: List[str] = Field(default_factory=list, description="Relevant coursework explicitly listed on the resume")
    start_date: Optional[date] = Field(None, description="Education start date, such as 'Sep 2020', '09/2020', or '2020'")
    end_date: Optional[date] = Field(None, description="Education end date, expected graduation date, or 'Present' if currently enrolled")

class Experience(BaseModel):
    title: Optional[str] = Field(None, description="Job title or position")
    organization: Optional[str] = Field(None, description="Employer, company, or organization name")
    location: Optional[str] = Field(None, description="City, state, province, country, or remote")
    start_date: Optional[date] = Field(None, description="Employment start date, such as 'Jan 2022', '01/2022', or '2022'")
    end_date: Optional[date] = Field(None, description="Employment end date or 'Present' if currently employed")
    current_job: Optional[bool] = Field(None, description="True if this is the candidate's current job")
    bullet_points: List[str] = Field(default_factory=list, description="Responsibilities, accomplishments, and achievements listed for this role")

class Project(BaseModel):
    name: Optional[str] = Field(None, description="Project name")
    description: Optional[str] = Field(None, description="Short description or summary of the project")
    technologies: List[str] = Field(default_factory=list, description="Programming languages, frameworks, tools, or technologies used")
    links: List[str] = Field(default_factory=list, description="Project URLs such as GitHub repositories, demos, or websites")
    bullet_points: List[str] = Field(default_factory=list, description="Additional project details, accomplishments, or features")

class SkillCategory(BaseModel):
    category: Optional[str] = Field(None, description="Skill category such as 'Languages', 'Frameworks', 'Tools', or 'Databases'")
    skills: List[str] = Field(default_factory=list, description="Skills belonging to this category")

class Certification(BaseModel):
    name: Optional[str] = Field(None, description="Certification name")
    issuer: Optional[str] = Field(None, description="Organization that issued the certification")
    issue_date: Optional[date] = Field(None, description="Date the certification was issued")
    expiration_date: Optional[date] = Field(None, description="Certification expiration date, if applicable")
    credential_id: Optional[str] = Field(None, description="Credential or certificate ID")
    url: Optional[str] = Field(None, description="Verification URL for the certification")

class Publication(BaseModel):
    title: Optional[str] = Field(None, description="Publication title")
    authors: List[str] = Field(default_factory=list, description="Authors listed for the publication")
    venue: Optional[str] = Field(None, description="Conference, journal, or publication venue")
    publisher: Optional[str] = Field(None, description="Publisher or publishing organization")
    publication_date: Optional[date] = Field(None, description="Publication date")
    url: Optional[str] = Field(None, description="URL where the publication can be accessed")

class Award(BaseModel):
    name: Optional[str] = Field(None, description="Award or honor name")
    issuer: Optional[str] = Field(None, description="Organization granting the award")
    award_date: Optional[date] = Field(None, description="Date the award was received")
    description: Optional[str] = Field(None, description="Description or reason for receiving the award")

class CustomSection(BaseModel):
    title: Optional[str] = Field(None, description="Custom section title")
    entries: List[str] = Field(default_factory=list, description="Raw text entries belonging to this custom section")

class EducationOutput(BaseModel):
    educations: List[Education] = Field(default_factory=list)

class ExperienceOutput(BaseModel):
    experiences: List[Experience] = Field(default_factory=list)

class ProjectOutput(BaseModel):
    projects: List[Project] = Field(default_factory=list)

class SkillOutput(BaseModel):
    skill_categories: List[SkillCategory] = Field(default_factory=list)

class CertificationOutput(BaseModel):
    certifications: List[Certification] = Field(default_factory=list)

class PublicationOutput(BaseModel):
    publications: List[Publication] = Field(default_factory=list)

class AwardOutput(BaseModel):
    awards: List[Award] = Field(default_factory=list)

class CustomSectionOutput(BaseModel):
    custom_sections: List[CustomSection] = Field(default_factory=list)

class ParsedResume(BaseModel):
    basics: Optional[Basics] = None
    educations: List[Education] = Field(default_factory=list)
    experiences: List[Experience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    skill_categories: List[SkillCategory] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)
    publications: List[Publication] = Field(default_factory=list)
    awards: List[Award] = Field(default_factory=list)
    custom_sections: List[CustomSection] = Field(default_factory=list)