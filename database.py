import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
engine = None
SessionLocal = None

def get_app_db_url():
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def init_engine():
    global engine, SessionLocal
    engine = create_engine(get_app_db_url())
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_table():
    if engine is None:
        raise RuntimeError("Engine not initialized. Call init_engine() first.")

    Base.metadata.create_all(bind=engine)


def get_db():
    if SessionLocal is None:
        raise RuntimeError("SessionLocal not initialized. Call init_engine() first.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()