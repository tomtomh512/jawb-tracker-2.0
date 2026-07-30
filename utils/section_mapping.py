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
        "field": "projects",
    },
    "skill_category": {
        "model": SkillOutput,
        "field": "skill_categories",
    },
    "certification": {
        "model": CertificationOutput,
        "field": "certifications",
    },
    "publication": {
        "model": PublicationOutput,
        "field": "publications",
    },
    "award": {
        "model": AwardOutput,
        "field": "awards",
    },
    "custom_section": {
        "model": CustomSectionOutput,
        "field": "custom_sections",
    },
}