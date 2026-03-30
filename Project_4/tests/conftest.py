from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from core.database import Base, get_db
from typing import Generator
from main import app

class TestSettings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env.test"

test_settings = TestSettings()

engine = create_engine(
    test_settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)