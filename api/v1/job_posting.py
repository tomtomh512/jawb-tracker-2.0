from fastapi import APIRouter

router = APIRouter(
    prefix="/job-postings",
    tags=["job postings"]
)


@router.get("/")
def get_job_postings():
    pass

@router.get("/{job_posting_id}")
def get_job_posting():
    pass

@router.post("/")
def create_job_posting():
    pass

@router.post("/parse")
def parse_job_posting():
    pass

@router.post("/{job_posting_id}/score")
def create_job_posting_score():
    pass

@router.post("/{job_posting_id}/cover-letter")
def create_job_posting_cover_letter():
    pass

@router.patch("/{job_posting_id}")
def update_job_posting():
    pass

@router.delete("/{job_posting_id}")
def delete_job_posting():
    pass