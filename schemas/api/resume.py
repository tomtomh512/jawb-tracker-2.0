from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from schemas.api.award import AwardCreate, AwardResponse
from schemas.api.certification import CertificationCreate, CertificationResponse
from schemas.api.custom_section import CustomSectionCreate, CustomSectionResponse
from schemas.api.education import EducationCreate, EducationResponse
from schemas.api.experience import ExperienceCreate, ExperienceResponse
from schemas.api.project import ProjectCreate, ProjectResponse
from schemas.api.publication import PublicationCreate, PublicationResponse
from schemas.api.skill_category import SkillCategoryCreate, SkillCategoryResponse


class ResumeBase(BaseModel):
    resumeName: str
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    summary: str | None = None
    websites: list[str] = Field(default_factory=list)


class ResumeCreate(ResumeBase):
    educations: list[EducationCreate] = Field(default_factory=list)
    experiences: list[ExperienceCreate] = Field(default_factory=list)
    projects: list[ProjectCreate] = Field(default_factory=list)
    skill_categories: list[SkillCategoryCreate] = Field(default_factory=list)
    certifications: list[CertificationCreate] = Field(default_factory=list)
    publications: list[PublicationCreate] = Field(default_factory=list)
    awards: list[AwardCreate] = Field(default_factory=list)
    custom_sections: list[CustomSectionCreate] = Field(default_factory=list)


class ResumeUpdate(ResumeBase):
    pass


class ResumeResponse(ResumeBase):
    id: UUID
    is_main: bool
    updated_at: datetime

    educations: list[EducationResponse] = Field(default_factory=list)
    experiences: list[ExperienceResponse] = Field(default_factory=list)
    projects: list[ProjectResponse] = Field(default_factory=list)
    skill_categories: list[SkillCategoryResponse] = Field(default_factory=list)
    certifications: list[CertificationResponse] = Field(default_factory=list)
    publications: list[PublicationResponse] = Field(default_factory=list)
    awards: list[AwardResponse] = Field(default_factory=list)
    custom_sections: list[CustomSectionResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ResumeTextCreate(BaseModel):
    resume_name: str
    content: str