import datetime
import pytz
from models.database import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, String, Time, DATETIME


def time():
    timezone = pytz.timezone('Asia/Tehran')
    now = datetime.datetime.now(timezone)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    qualify = Column(Integer)
    user = Column(Integer)
    restaurant = Column(Integer)
    datatime = Column(DATETIME, default=time())
    is_payment = Column(Boolean, default=False)
