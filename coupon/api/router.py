from fastapi import APIRouter, status, HTTPException, Depends, Request, Body
from models.dependencies import get_db
from sqlalchemy.orm import Session
from schemas.schema import Coupon
import requests
import json

router = APIRouter()

# url = 'http://127.0.0.1:8888/show/model/user/'
# r = requests.post(url)
# rrr = json.loads(r.content)
# list_users = rrr['user']
# print('I' * 50)
#
# for item in list_users:
#     print(item['phone_number'])
#
# print('I' * 50)

