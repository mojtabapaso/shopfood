from pydantic import BaseModel, Json
from typing import Dict


class UserRestaurant(BaseModel):
    users: Dict


class FoodAdd(BaseModel):
    name: str
    price: int
