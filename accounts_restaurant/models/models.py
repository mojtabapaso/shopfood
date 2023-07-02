from models.database import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, String
from datetime import datetime


class OtpCode(Base):
    __tablename__ = 'otp_code_restaurant'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(7), index=True)
    expired = Column(Boolean, default=True)
    phone_number = Column(String(11), index=True)
    time = Column(DateTime, default=datetime.now)


class UserRestaurant(Base):
    __tablename__ = 'user_restaurant'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(11), unique=True, index=True)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    name = Column(String)
    password = Column(String, nullable=True)
