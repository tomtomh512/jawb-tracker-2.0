from fastapi import APIRouter
from api.v1.resume import router as resumes_router
from api.v1.education import router as education_router
from api.v1.experience import router as experience_router
from api.v1.award import router as award_router
from api.v1.certification import router as certification_router
from api.v1.custom_section import router as custom_section_router
from api.v1.project import router as project_router
from api.v1.publication import router as publication_router
from api.v1.skill_category import router as skill_category_router

from api.v1.job_posting import router as job_posting_router

from api.v1.note import router as note_router

api_router = APIRouter()

api_router.include_router(resumes_router)
api_router.include_router(education_router)
api_router.include_router(experience_router)
api_router.include_router(award_router)
api_router.include_router(custom_section_router)
api_router.include_router(project_router)
api_router.include_router(publication_router)
api_router.include_router(skill_category_router)
api_router.include_router(certification_router)

api_router.include_router(job_posting_router)

api_router.include_router(note_router)