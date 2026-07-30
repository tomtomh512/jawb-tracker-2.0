from fastapi import APIRouter
from api.v1.resumes.resume import router as resumes_router
from api.v1.resumes.education import router as education_router
from api.v1.resumes.experience import router as experience_router

api_router = APIRouter()

api_router.include_router(resumes_router)
api_router.include_router(education_router)
api_router.include_router(experience_router)
