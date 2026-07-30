from uuid import UUID

from sqlalchemy.orm import Session

from models.resume import (
    Resume,
    Education,
    Experience,
    Project,
    SkillCategory,
    Certification,
    Publication,
    Award,
    CustomSection,
)
from schemas.api.resume import ResumeCreate


def get_resumes(db: Session):
    return db.query(Resume).all()


def get_resume(db: Session, resume_id: UUID):
    return db.query(Resume).filter(Resume.id == resume_id).first()


def create_resume(db: Session, resume: ResumeCreate):
    db_resume = Resume(
        resumeName=resume.resumeName,
        name=resume.name,
        email=resume.email,
        phone=resume.phone,
        location=resume.location,
        summary=resume.summary,
        websites=resume.websites,
        education=[Education(**e.model_dump()) for e in resume.education],
        experience=[Experience(**e.model_dump()) for e in resume.experience],
        projects=[Project(**p.model_dump()) for p in resume.projects],
        skill_categories=[SkillCategory(**s.model_dump()) for s in resume.skill_categories],
        certifications=[Certification(**c.model_dump()) for c in resume.certifications],
        publications=[Publication(**p.model_dump()) for p in resume.publications],
        awards=[Award(**a.model_dump()) for a in resume.awards],
        custom_sections=[CustomSection(**cs.model_dump()) for cs in resume.custom_sections],
    )

    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume


def update_resume():
    pass


def delete_resume():
    pass