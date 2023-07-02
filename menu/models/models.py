from sqlalchemy.orm import relationship
from models.database import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, String, ForeignKey
from datetime import datetime


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True, index=True)
    user_restaurant_id = Column(Integer, index=True)
    score = Column(Integer, default=None)
    Income = Column(Integer, default=0)
    name = Column(String, nullable=True)


class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    restaurant = Column(ForeignKey("restaurant.id"), index=True)
    user = relationship("Restaurant", backref="foods")
