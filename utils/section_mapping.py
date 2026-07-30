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
    "projects": {
        "model": ProjectOutput,
        "field": "projects",
    },
    "skills": {
        "model": SkillOutput,
        "field": "skills",
    },
    "certification": {
        "model": CertificationOutput,
        "field": "certifications",
    },
    "publication": {
        "model": PublicationOutput,
        "field": "publications",
    },
    "awards": {
        "model": AwardOutput,
        "field": "awards",
    },
    "custom": {
        "model": CustomSectionOutput,
        "field": "custom_sections",
    },
}