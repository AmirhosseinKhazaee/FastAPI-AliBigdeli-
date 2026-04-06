from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from core.database import Base, get_db
from typing import Generator
from main import app
from pytest import fixture

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

@fixture(scope="module")
def db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture(scope="module",autouse=True)
def override_dependencies(db_session):
    app.dependency_overrides[get_db] =lambda : db_session
    yield
    app.dependency_overrides.pop(get_db ,None)


@fixture(scope="session",autouse=True)
def tear_up_and_down_database():
    Base.metadata.create_all(bind=engine)
    yield 
    Base.metadata.drop_all(bind=engine)

@fixture(scope="function")
def annon_client():
    client = TestClient(app)
    yield client
