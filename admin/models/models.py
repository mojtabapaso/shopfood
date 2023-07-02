from models.database import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, String
from core.time import time


# class StatusAccess(Base):
#     __tablename__ = 'otp_code_admin'
#     id = Column(Integer, primary_key=True, index=True)
#     status = Column(String)


class UserAdmin(Base):
    __tablename__ = 'user_admin'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(Integer)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
