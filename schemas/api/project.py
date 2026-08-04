from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str | None = None
    description: str | None = None
    skills: list[str] | None = Field(default_factory=list)
    links: list[str] | None = Field(default_factory=list)
    bullet_points: list[str] | None = Field(default_factory=list)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)