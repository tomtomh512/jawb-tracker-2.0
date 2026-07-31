from typing import List, Optional

from pydantic import BaseModel, Field


class RubricItem(BaseModel):
    name: str = Field(...,description="Short name of the evaluation category")
    description: str = Field(...,description="What this category measures")
    importance: int = Field(
        ...,
        ge=0,
        le=10,
        description=(
            "Importance score from 0 to 10:\n"
            "- 0 = Not important\n"
            "- 1-3 = Nice to have\n"
            "- 4-6 = Moderately important\n"
            "- 7-9 = Very important\n"
            "- 10 = Critical / required"
        )
    )
    required: bool = Field(False, description="Whether this category is a hard requirement")
    evidence_sources: List[str] = Field(default_factory=list, description="Resume sections the scorer should consider, such as experience, projects, education, skills, certifications, or publications")
    keywords: List[str] = Field(default_factory=list, description="Important technologies or concepts associated with this category")
    minimum_years: Optional[int] = Field(None, description="Minimum years of experience expected for this category")

class Rubric(BaseModel):
    items: List[RubricItem] = Field(default_factory=list, description="Evaluation rubric generated from the job posting")

class ScoredRubricItemLLMOutput(BaseModel):
    score: float = Field(
        ...,
        ge=0,
        le=10,
        description="0 = no evidence, 10 = exceptional evidence"
    )
    reasoning: str = Field(..., description="Brief justification for the score")
    evidence: List[str] = Field(default_factory=list, description="Specific resume snippets (bullet points, skills, etc.) that informed the score")
    strengths: List[str] = Field(default_factory=list, description="Key strengths that positively impacted this rubric item's score")
    weaknesses: List[str] = Field(default_factory=list, description="Missing qualifications, gaps, or weaknesses that reduced this rubric item's score")

class ScoredRubricItem(BaseModel):
    name: str
    description: str
    importance: int
    required: bool
    weight: float
    score: float
    weighted_score: float
    reasoning: str
    evidence: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)


class ScoredRubric(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    overall_score: float
    items: List[ScoredRubricItem] = Field(default_factory=list)
    missing_required: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)