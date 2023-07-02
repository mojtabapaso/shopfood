import json
from typing import Dict

import requests
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi_jwt_auth import AuthJWT, exceptions
from fastapi_jwt_auth.exceptions import *
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.dependencies import get_db
from models.models import Restaurant, Food
from core.schemas.schema import FoodAdd

router = APIRouter()


# url_1 = "http://127.0.0.1:1500/register/phone/"
# url_1 = "http://127.0.0.1:1500/show/model/user/"
# url_2 = "http://127.0.0.1:2500/res/users/"
# # url = "http://127.0.0.1:3500/"

# er = requests.options(url_1)
# js = json.loads(er.content)
# js = js['user']
# print('I' * 50)
# for item in js:
#     print(item['phone_number'])
# print('I' * 50)
# datas = json.loads(requests.options(url_2).content)
# print(datas)
# print("I" * 50)

class Settings(BaseModel):
    authjwt_secret_key: str = "JWT###Restaurant###Menu###wq3pi97delfcn_yu=yhv12mid15671df*df7dfd7hgf213dg1j1l7p411ef"
    # Secret Key Json Web Token
    # :)
    authjwt_token_location = ("headers",)
    authjwt_cookie_secure = False
    authjwt_algorithm = "HS256"


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post('/get/user/res/')
def user_restaurant(users: Dict, db: Session = Depends(get_db)):
    res = db.query(Restaurant).filter(Restaurant.user_restaurant_id == users['id']).first()
    if res:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    restaurant = Restaurant(user_restaurant_id=users['id'])
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)


@router.post('/add/menu/food/', status_code=status.HTTP_201_CREATED)
def add_food(data: FoodAdd, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        phone_number = Authorize.get_jwt_subject()

        # ------------------------------------------------
        req = requests.get(f"http://127.0.0.1:2500/get/data/user/{phone_number}/")
        user_restaurant = json.loads(req.content)
        id = user_restaurant['id']
        # -------------------------------------------------

        food_id_exist = db.query(Food).filter(Food.name == data.name)
        for item in food_id_exist:
            if item.restaurant == id:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This name already used")
        food = Food(name=data.name, price=data.price, restaurant=id)
        db.add(food)
        db.commit()
        db.refresh(food)
        return {'detail': f'Food {data.name} added successfully'}
    except JWTDecodeError or MissingTokenError or AuthJWTException:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Json Web Token invalid')


@router.get("/show/list/food/{restaurant_id}/")
def show_menu(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant_menu = db.query(Food).filter(Food.restaurant == restaurant_id)
    for item in restaurant_menu:
        yield item


@router.get("/show/list/restaurants/")
def show_restaurant(db: Session = Depends(get_db)):
    restaurants = db.query(Restaurant).all()
    for item in restaurants:
        yield item


@router.post("/add/cart/{id_restaurant}/{id_food}", status_code=status.HTTP_201_CREATED)
def add_cart(id_restaurant: int, id_food: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        phone_number = Authorize.get_jwt_subject()
        # -----------------get Id user from microservice accounts_client -------------
        request = requests.post(f"http://127.0.0.1:1500/show/id/user/{phone_number}")
        json_content = json.loads(request.content)
        id_user = json_content["user_id"]
        # ---------------- send id_food ,id_restaurant ,id_user to microservice cart
        data = {"id_food": str(id_food), "id_restaurant": str(id_restaurant), "id_user": str(id_user)}
        requests.post('http://127.0.0.1:5500/add/cart/', json=data)
    except JWTDecodeError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Auth JWT Exception')


@router.post("/remove/cart/{id_restaurant}/{id_food}", status_code=status.HTTP_201_CREATED)
def add_cart(id_restaurant: int, id_food: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        phone_number = Authorize.get_jwt_subject()
        # -----------------get Id user from microservice accounts_client -------------
        request = requests.post(f"http://127.0.0.1:1500/show/id/user/{phone_number}")
        json_content = json.loads(request.content)
        id_user = json_content["user_id"]
        # ---------------- send id_food ,id_restaurant ,id_user to microservice cart
        data = {"id_food": str(id_food), "id_restaurant": str(id_restaurant), "id_user": str(id_user)}
        requests.post('http://127.0.0.1:5500/remove/cart/', json=data)
    except JWTDecodeError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Auth JWT Exception')
