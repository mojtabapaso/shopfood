import json

from fastapi import FastAPI, WebSocket, Depends, APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import asyncio
import websockets
from models.models import User, Profile, OtpCode
from pydantic.schema import date
from sqlalchemy.orm import Session

from models.dependencies import get_db
from starlette import status

socket = APIRouter()


#
def create_list_from_model_row(data):
    list_data = []
    for item in data:
        otp_code_dict = item.__dict__
        del otp_code_dict['_sa_instance_state']
        list_data.append(otp_code_dict)
    return list_data


def user_to_dict(user):
    return {"id": user.id, "phone_number": user.phone_number, "is_active": user.is_active,
            "password": user.password}


@socket.websocket("/users/")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    try:
        await websocket.accept()
        users = db.query(User).order_by(User.id.desc()).limit(15).all()
        json = [user_to_dict(user) for user in users]
        json = {"detail": json}
        await websocket.send_json(json)
    except AttributeError:
        await websocket.send_json({"detail": {"Warning": "This DataBase is empty"}})


def profile_to_dict(profile):
    return {"id": profile.id, "email": profile.email, "first_name": profile.first_name,
            "last_name": profile.last_name, "password": profile.password}


@socket.websocket("/profiles/")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    try:
        await websocket.accept()
        profiles = db.query(Profile).order_by(Profile.id.desc()).limit(15).all()
        json = [profile_to_dict(profile) for profile in profiles]
        json = {"detail": json}
        await websocket.send_json(json)
    except AttributeError:
        await websocket.send_json({"detail": {"Warning": "This DataBase is empty"}})


import json


@socket.websocket("/otps/")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    try:
        await websocket.accept()
        otp_codes = db.query(OtpCode).order_by(OtpCode.id.desc()).limit(15).all()
        list_data = create_list_from_model_row(otp_codes)
        json = {"detail": str(list_data)}
        await websocket.send_json(json)
    except AttributeError:
        await websocket.send_json({"detail": {"Warning": "This DataBase is empty"}})


@socket.websocket("/deactivate/user/")
async def websocket_deactivate_user(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    json_data = await websocket.receive_json()
    id_user = json_data["id"]
    user = db.query(User).filter(User.id == int(id_user)).first()
    if user is None:
        await websocket.send_json({"message": "user not found.", "status": status.HTTP_409_CONFLICT})
    if user.is_active is False:
        await websocket.send_json({"message": "user already deactivate", "status": status.HTTP_400_BAD_REQUEST})
    user.is_active = False
    db.commit()
    db.refresh(user)
    await websocket.send_json({"message": "user deactivate successfully.", "status": status.HTTP_200_OK})


@socket.websocket("/activate/user/")
async def websocket_activate_user(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    json_data = await websocket.receive_json()
    id_user = json_data["id"]
    user = db.query(User).filter(User.id == int(id_user)).first()
    if user is None:
        await websocket.send_json({"message": "user not found.", "status": status.HTTP_409_CONFLICT})
    if user.is_active:
        await websocket.send_json({"message": "user already activate", "status": status.HTTP_400_BAD_REQUEST})
    user.is_active = True
    db.commit()
    db.refresh(user)
    await websocket.send_json({"message": "user activate successfully.", "status": status.HTTP_200_OK})
