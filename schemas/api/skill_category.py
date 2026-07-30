from pydantic import BaseModel, ConfigDict, Field


class SkillCategoryBase(BaseModel):
    category: str | None = None
    skills: list[str] | None = Field(default_factory=list)


class SkillCategoryCreate(SkillCategoryBase):
    pass


class SkillCategoryUpdate(SkillCategoryBase):
    pass


class SkillCategoryResponse(SkillCategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)