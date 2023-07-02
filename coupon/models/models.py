from core.models.database import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, String
from datetime import datetime
from core.utils.coupon import create_coupon


class OtpCode(Base):
    __tablename__ = 'coupon'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(11), default=create_coupon, index=True)
    expired = Column(Boolean, default=True)
    user = Column(String(11), index=True)
    time = Column(DateTime, default=datetime.now)
