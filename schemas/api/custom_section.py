from pydantic import BaseModel, ConfigDict, Field


class CustomSectionBase(BaseModel):
    title: str | None = None
    entries: list[str] | None = Field(default_factory=list)


class CustomSectionCreate(CustomSectionBase):
    pass


class CustomSectionUpdate(CustomSectionBase):
    pass


class CustomSectionResponse(CustomSectionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)