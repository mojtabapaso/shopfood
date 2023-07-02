from typing import Dict
from fastapi import APIRouter
from datetime import datetime
import pytz
from fastapi_jwt_auth import AuthJWT

router = APIRouter()


@router.post('/add/cart/')
def add_cart(data: Dict):
    print("I" * 50)
    print(data["id_user"])
    print("I" * 50)
# /remove/cart/

@router.post('/remove/cart/')
def add_cart(data: Dict):
    print("I" * 50)
    print(data["id_user"])
    print("I" * 50)