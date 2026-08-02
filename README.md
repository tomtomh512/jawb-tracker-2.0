# Jawb Tracker 2.0

## Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Running the App](#running-the-app)
- [Resume LLM Flows](#resume-llm-flows)
- [Job Posting LLM Flows](#job-posting-llm-flows)
- [Database & Migrations](#database--migrations)
- [Project Structure](#project-structure)

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- React (Frontend sample)

## Prerequisites

- Python 3.11+
- PostgreSQL
- Node.js 18+
- API keys for LLM provider:
  - Google Gemini

## Local Setup

### 1. Clone and install backend dependencies

```bash
git clone https://github.com/tomtomh512/jawb-tracker-2.0.git
cd jawb-tracker-2.0

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Create the database

```bash
CREATE DATABASE jawb_tracker
```

### 3. Configure environment variables

Create a `.env` file in the repo root:

```dotenv
# Gemini (primary/default LLM provider)
GEMINI_API_KEY=your_gemini_api_key
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_MODEL=gemini-3.1-flash-lite

# or some other alternate LLM provider

# Postgres connection
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=jawb_tracker
DB_HOST=localhost
DB_PORT=5432
```

### 4. (Optional) Install frontend website dependencies

```bash
cd sample_frontend/website
npm install
```

### 5. (Optional) Install desktop app dependencies

```bash
cd sample_frontend/desktop-app
npm install
```

### 6. (Optional) Load the Chrome extension

1. Go to `chrome://extensions`, enable Developer Mode.
2. Click "Load unpacked" and select the `sample_frontend/extension` folder.

## Running the App

**Backend:**

```bash
uvicorn main:app --reload
```

**(Optional) Frontend:**

```bash
cd sample_frontend/website
npm run dev
```

**(Optional) Frontend:**

```bash
cd sample_frontend/desktop-app
npm run electron:dev
```

## Resume LLM Flows

Resume parsing (`utils/resume_parser.py`) turns free-text or a PDF resume into a fully structured `ParsedResume` object using a **two-pass extraction** strategy, all routed through `LLMManager`:

1. **Initial scan** (`initialResumeScanText` / `initialResumeScanPdf`) — a single LLM call extracts:
   - `basics`: name, email, phone, location, summary, personal/portfolio links
   - `resume_sections`: every detected section, each classified into one of `education`, `experience`, `project`, `skill_category`, `certification`, `publication`, `award`, or `custom_section`, with the raw text preserved per entry.

   PDFs are handled by uploading the file directly to Gemini (`prompt_pdf`) rather than extracting text first, so formatting-heavy resumes are read as-is.

2. **Per-section structured extraction** (`parse_section` → `assemble_parsed_resume`) — each classified section is expanded concurrently (max 2 in-flight requests via an `asyncio.Semaphore`) into its full schema, e.g. an `experience` section becomes a list of `Experience` objects with title, organization, dates, and bullet points. The mapping from classification → output schema lives in `utils/section_mapping.py`. Results are merged back into one `ParsedResume`.

Entry points:
- `parse_resume_from_text(resume_text, llm_model="gemini")`
- `parse_resume_from_pdf(pdf_path, llm_model="gemini")`

Exposed via the API (`api/v1/resume.py`):
- `POST /api/v1/resumes/parse` — parse pasted resume text
- `POST /api/v1/resumes/parsePdf` — parse an uploaded PDF (multipart form, 10 MB max)

## Job Posting LLM Flows

Job postings go through three independent LLM-backed steps, all orchestrated from `services/job_posting_service.py`:

### 1. Parsing (`utils/job_posting_parser.py`)

`parse_job_posting_from_text` sends the raw posting text to the LLM and extracts a `ParsedJobPosting`: title, company, location (with remote/hybrid detail), employment type, responsibilities, requirements, skills, education requirements, compensation (salary range, currency, period, bonus, equity), visa sponsorship, and clearance requirements. The result is persisted as a `JobPosting` row, alongside the original raw text.

### 2. Cover letter generation (`utils/cover_letter_generator.py`)

`generate_cover_letter(resume, job_posting, custom_prompt=None)` prompts the LLM to write a tailored cover letter with the resume treated as the **only source of truth** about the candidate. An optional `custom_prompt` lets the user steer tone/content.

### 3. Resume scoring (`utils/score.py`)

Scoring is a two-stage process:
- **Rubric generation** (`generate_rubric`) — the LLM acts as a hiring manager and generates 5–10 weighted evaluation categories (`RubricItem`s) from the job posting, explicitly avoiding generic/filler categories (communication, teamwork, etc.) unless they're clearly central to the role.
- **Per-item scoring** (`score_rubric_item`, run concurrently with a semaphore of 2) — each rubric item is scored 0–10 against the candidate's structured resume JSON, with reasoning, cited evidence, strengths, and weaknesses returned per item.

Weights are normalized (`utils/normalize_weights.py`) so they sum to 1, and the final `overall_score` is the weighted sum of item scores, scaled to 0–100. Required rubric items scored below 5 are surfaced as `missing_required`.

## Database & Migrations

Schema changes are managed with Alembic:

```bash
# after changing a model in models/
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

`alembic/env.py` builds its own Postgres URL from the same `DB_*` environment variables as `database.py`, so no separate Alembic-specific configuration is needed beyond `.env`.

## Project Structure

```
api/v1/          FastAPI routers (one per resource)
services/        Business logic + DB access, called by routers
models/          SQLAlchemy ORM models
schemas/api/     Pydantic request/response schemas for the REST API
schemas/llm/     Pydantic schemas used as structured LLM output targets
llm/             Provider-agnostic LLM manager + per-provider clients
utils/           Resume/job posting parsing, scoring, cover letter generation, backups
alembic/         Database migrations
sample_frontend/website    Reference React + Vite client
sample_frontend/extension  Reference Chrome extension client
```

## Todos

- Docker integration
- Testing