from fastapi.params import Depends
from fastapi.testclient import TestClient
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from project.models.database import Base
from project.core.config import app
import pytest
from project.api.accounts_client.router import get_db
from project.models.accounts_client.models import User, OtpCode, Profile
from unittest.mock import MagicMock
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from kavenegar import HTTPException, APIException

client = TestClient(app)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = TestingSessionLocal()

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


db = override_get_db()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def model():
    pass


# @pytest.fixture(scope="function")
# def db_testing(model):
#     user = User(phone_number='09123333333', is_active=True, password="password_test")
#     code = OtpCode(code="12345", phone_number="09123333333")
#     session.add(user, code)
#     session.commit()
@pytest.fixture(scope='function')
def db_testing():
    user = session.query(User).filter_by(phone_number='09123333333').first()
    if user is None:
        user = User(phone_number='09123333333', is_active=True, password="password_test")
        session.add(user)

    code = session.query(OtpCode).filter_by(phone_number='09123333333').first()
    if code is None:
        code = OtpCode(code="123456", phone_number="09123333333")
        session.add(code)

    session.commit()


@pytest.fixture(scope='session')
def close_all():
    session.query(User).filter(User.is_active == True).delete()
    session.query(OtpCode).filter(OtpCode.expired == True).delete()
    session.commit()
    yield close_all




def test_get_code_and_send(db_testing, close_all):
    data = {"phone_number": "09123333333"}
    response = client.post("/login/phone/", json=data)
    assert response.status_code == 201
    assert response.json() == "We send opt code for your phone number code"
    # --------------
    # response = client.post("/login/phone/", json=data)
    # assert response.status_code == 429
    # assert response.json() == {'detail': 'Please wait for 2 minutes before requesting a new OTP'}
    # ---------------
    data = {"phone_number": "09123333331"}
    response = client.post("/login/phone/", json=data)
    assert response.status_code == 404


def test_login_and_token(db_testing, close_all):
    data = {"code": "123456", "phone_number": "09123333333"}
    response = client.post("/login/code/", json=data)
    assert response.status_code == 200
    data = {"code": "123456", "phone_number": "0912111112"}
    response = client.post("/login/code/", json=data)
    assert response.status_code == 404
    data = {"code": "", "phone_number": ""}
    response = client.post("/login/code/", json=data)
    assert response.status_code == 422
    response = client.post("/login/code/")
    assert response.status_code == 422

# @pytest.fixture
# def create_value_in_data_base(model):
#     user = User(phone_number='0912111111', is_active=True, password="password_test")
#     code = OtpCode(code="12345", phone_number="0912111111")
#     session.add(user, code)
#     session.commit()
