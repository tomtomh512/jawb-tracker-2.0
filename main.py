from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler

from slowapi.errors import RateLimitExceeded

from limiter import limiter
from api.router import api_router
from database import create_table, init_engine
from utils.backup import run_backup_if_needed


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_engine()
    create_table()
    run_backup_if_needed()
    yield

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # change later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")