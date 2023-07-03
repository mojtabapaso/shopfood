from fastapi.testclient import TestClient
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.models.database import Base
from project.core.config import app
import pytest
from project.api.accounts_client.router import get_db

faker = Faker()

client = TestClient(app)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db


def test_login_phone_number(test_db):
    data = {"code": "123456", "phone_number": "09331264965"}
    response = client.post("/login/phone/", json=data)
    assert response.status_code == 200


def test_testing():
    response = client.post("/a/")
    assert response.status_code == 200


def test_testing2():
    response = client.get("/b/")
    assert response.status_code == 200
