from schemas.llm.resume import (
    EducationOutput,
    ExperienceOutput,
    ProjectOutput,
    SkillOutput,
    CertificationOutput,
    PublicationOutput,
    AwardOutput,
    CustomSectionOutput,
)


SECTION_MAPPING = {
    "education": {
        "model": EducationOutput,
        "field": "education",
    },
    "experience": {
        "model": ExperienceOutput,
        "field": "experience",
    },
    "project": {
        "model": ProjectOutput,
        "field": "project",
    },
    "skill_category": {
        "model": SkillOutput,
        "field": "skill_category",
    },
    "certification": {
        "model": CertificationOutput,
        "field": "certification",
    },
    "publication": {
        "model": PublicationOutput,
        "field": "publication",
    },
    "award": {
        "model": AwardOutput,
        "field": "award",
    },
    "custom_section": {
        "model": CustomSectionOutput,
        "field": "custom_section",
    },
}