from datetime import datetime, timedelta
from random import randint

import pytz
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://fast:fast@localhost:5432/testapi'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./SQLite.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
metadata = MetaData()
database = Base()

# ____________________________________________________

from typing import Dict, List, Any
from sqlalchemy.orm import Session
# from models.data.sqlalchemy_models import Signup
from models.models import User, OtpCode, Profile
from sqlalchemy import desc
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from core.utils.sender import send_otp_code

pytz.timezone('Asia/Tehran')


def validate_phone_number(phone_number):
    if len(phone_number) != 11:
        return False
    if not phone_number.isdigit():
        return False
    return True


# await
class UserModel:
    def __init__(self, session: Session):
        self.db: Session = session

    async def validate_user(self, phone_number):

        if validate_phone_number(phone_number=str(phone_number)) is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This phone number invalid")

        user_exist = self.db.query(User).filter(User.phone_number == str(phone_number)).first()
        if user_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This user already exist")

    async def create_user(self, phone_number):
        user = User(phone_number=phone_number)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

    def insert_user(self, user: User) -> bool:
        try:
            self.db.add(user)
            self.db.commit()
        except:
            return False
        return True

    def get_all_users(self):
        return self.db.query(User).all()


# def show(self, signup: User) -> bool:
#     try:
#         print(signup)
#         self.sess.add(signup)
#
#         self.sess.commit()
#     except:
#         return False
#     return True


# @router.get("/signup/list", response_model=List[SignupReq])
# def list_signup(db:Session = Depends(sess_db)):
#       repo:SignupRepository = SignupRepository(db)
#       result = repo.get_all_signup()
#       return result

class OtpModel:
    def __init__(self, session: Session):
        self.db: Session = session

    async def validate_otp(self, phone_number: str):
        otp_code = self.db.query(OtpCode).filter(OtpCode.phone_number == str(phone_number)).order_by(
            OtpCode.id.desc()).first()

        if otp_code and (otp_code.time + timedelta(minutes=2)) > datetime.now():
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                detail='Please wait for 2 minutes before requesting a new OTP')

    def validate_otp_after_send(self, phone_number: str, code: str):
        user_code = self.db.query(OtpCode).filter(
            OtpCode.phone_number == str(phone_number) and OtpCode.code == code).order_by(
            OtpCode.id.desc()).first()
        if user_code and (user_code.time + timedelta(minutes=2)) < datetime.now():
            user_code.expired = False
            self.db.commit()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The verification code has expired or invalid')
        self.db.delete(user_code)

    def false_otp_if_available(self, phone_number):
        db_otp = self.db.query(OtpCode).filter(OtpCode.phone_number == str(phone_number))
        if db_otp.first():
            db_otp.update({OtpCode.expired: False})
            self.db.commit()

    def create_otp(self, phone_number):
        self.otpCode = OtpCode(code=randint(10000, 99999), phone_number=phone_number)
        self.db.add(self.otpCode)
        self.db.commit()
        self.db.refresh(self.otpCode)

    def send_otp(self):
        phone_number = self.otpCode.phone_number
        code = self.otpCode.code
        try:
            pass
            # send_otp_code(code, phone_number)
        except:
            raise HTTPException(detail="sorry server failed try sometime again",
                                status_code=status.HTTP_502_BAD_GATEWAY)


class ProfileModel:
    def __init__(self, session: Session):
        self.db: Session = session

    async def create_profile(self, phone_number: str):
        profile = Profile(phone_number=phone_number)
        self.db.add(instance=profile)
        self.db.commit()
        self.db.refresh(profile)
