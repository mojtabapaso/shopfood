from datetime import datetime
import pytz
from sqlalchemy.orm import relationship
from ..database import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, String, ForeignKey

pytz.timezone('Asia/Tehran')


def time():
    timezone = pytz.timezone('Asia/Tehran')
    now = datetime.now(timezone)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return current_time


class OtpCode(Base):
    __tablename__ = 'otp_code'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(7), index=True)
    expired = Column(Boolean, default=True)
    phone_number = Column(String(11), index=True)
    time = Column(DateTime, default=datetime.now())


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String(11), ForeignKey('users.phone_number'))
    user = relationship("User", backref="profiles")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(11), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    password = Column(String, nullable=True)
