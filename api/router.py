from fastapi import APIRouter
from api.v1.resume import router as resumes_router
from api.v1.education import router as education_router

api_router = APIRouter()

api_router.include_router(resumes_router)
api_router.include_router(education_router)
