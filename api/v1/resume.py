from fastapi import APIRouter
from schemas.api.resume import ResumeCreate

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"]
)


@router.get("/")
def get_resume():
    return "get resume"

@router.post("/")
def upload_resume(data: ResumeCreate):
    print(data.model_dump_json())
    return {"message": "Resume received", "data": data}

@router.post("/text")
def upload_resume_text():
    return "post resume text"

@router.post("/pdf")
def upload_resume_pdf():
    return "post resume pdf"

@router.patch("/{resume_id}")
def update_resume_pdf():
    return "patch resume"

@router.delete("/{resume_id}")
def delete_resume_pdf():
    return "delete resume"