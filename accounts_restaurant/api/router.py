import json
from datetime import timedelta, datetime
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import *
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.schemas import schema
from core.security.password_hasher import get_password_hash, verify_password
from models.dependencies import get_db
from models.models import UserRestaurant, OtpCode
from random import randint
import requests
from core.utils.sender import send_otp_code
from fastapi.responses import JSONResponse
router = APIRouter()


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


@router.post('/res/register/phone/', status_code=status.HTTP_200_OK)
def register_user_restaurant(data: schema.PhoneNumber, db: Session = Depends(get_db)):
    last_otp_time = db.query(OtpCode).filter(OtpCode.phone_number == data.phone_number).order_by(
        OtpCode.id.desc()).first()
    if last_otp_time and (last_otp_time.time + timedelta(minutes=2)) > datetime.now():
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail='Please wait for 2 minutes before requesting a new OTP')
    user = db.query(UserRestaurant).filter(UserRestaurant.phone_number == data.phone_number).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This phone Number already exist')
    code = randint(10000, 99999)
    otpCode = OtpCode(code=code, phone_number=data.phone_number)
    db.add(otpCode)
    db.commit()
    db.refresh(otpCode)
    send_otp_code(code, data.phone_number)
    return JSONResponse( f'We send opt code for your phone number | code  : {otpCode}',status_code=status.HTTP_201_CREATED)
#     only in production use upper JSONResponse
#     return JSONResponse( 'We send opt code for your phone number',status_code=status.HTTP_201_CREATED)

@router.post('/res/register/code/', status_code=status.HTTP_201_CREATED)
def register_and_token(data: schema.OtpCode, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user_code = db.query(OtpCode).filter(
        OtpCode.phone_number == data.phone_number and OtpCode.code == data.code).order_by(
        OtpCode.id.desc()).first()
    if user_code and (user_code.time + timedelta(minutes=2)) < datetime.now():
        user_code.expired = False
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='The verification code has expired or invalid')
    userRes = UserRestaurant(phone_number=data.phone_number)
    db.add(userRes)
    db.delete(user_code)
    db.commit()
    db.refresh(userRes)
    # ------------------------
    # send for microservice menu
    # create a model restaurant in microservice menu
    json_data = {'id': str(userRes.id), 'phone_number': str(userRes.phone_number), 'email': str(userRes.email),
                 'is_active': str(userRes.is_active),
                 'name': str(userRes.name), }
    requests.post('http://127.0.0.1:4500/get/user/res/', json=json_data)
    # ------------------------
    access_token = Authorize.create_access_token(subject=data.phone_number)
    refresh_token = Authorize.create_refresh_token(subject=data.phone_number)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post('/res/login/phone/', status_code=status.HTTP_200_OK)
def login_user_restaurant(data: schema.PhoneNumber, db: Session = Depends(get_db)):
    user_exist = db.query(UserRestaurant).filter(UserRestaurant.phone_number == data.phone_number).first()
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This phone number not found")
    last_otp_time = db.query(OtpCode).filter(OtpCode.phone_number == data.phone_number).order_by(
        OtpCode.id.desc()).first()
    if last_otp_time and (last_otp_time.time + timedelta(minutes=2)) > datetime.now():
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail='Please wait for 2 minutes before requesting a new OTP')
    otpCode = OtpCode(code=randint(10000, 99999), phone_number=data.phone_number)
    db.add(otpCode)
    db.commit()
    db.refresh(otpCode)
    send_otp_code(otpCode, data.phone_number)
    return JSONResponse(f'We send opt code for your phone number | code  : {otpCode}',status_code=status.HTTP_201_CREATED)


#     only in production use upper JSONResponse
#     return JSONResponse( 'We send opt code for your phone number',status_code=status.HTTP_201_CREATED)


@router.post('/res/login/code/', status_code=status.HTTP_200_OK)
def login_token(data: schema.OtpCode, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    user_exist = db.query(UserRestaurant).filter(UserRestaurant.phone_number == data.phone_number).first()
    if user_exist is None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="This phone number not found")
    code_valid = db.query(OtpCode).filter(OtpCode.code == data.code).first()
    if code_valid and (code_valid.time + timedelta(minutes=2)) < datetime.now():
        code_valid.expired = False
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='The verification code has expired or invalid')
    access_token = Authorize.create_access_token(subject=data.phone_number)
    refresh_token = Authorize.create_refresh_token(subject=data.phone_number)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("res/login/password/", status_code=status.HTTP_200_OK)
def login_password(data: schema.loginPassword, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    password = data.password
    phone_number = data.phone_number
    user = db.query(UserRestaurant).filter(UserRestaurant.phone_number == phone_number).first()
    verifyPassword = verify_password(password, user.password)
    if verifyPassword is False:
        return "password invalid"
    refresh_token = Authorize.create_refresh_token(subject=phone_number)
    access_token = Authorize.create_access_token(subject=phone_number)
    return {"access_token": access_token, 'refresh_token': refresh_token}


@router.post('/set/password/', status_code=status.HTTP_200_OK)
def set_password(data: schema.SetPassword, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
        if data.password != data.password2:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Two Password be most mach')
        phone_number = Authorize.get_jwt_subject()
        user = db.query(UserRestaurant).filter(UserRestaurant.phone_number == phone_number).first()
        hash_password = get_password_hash(data.password)
        user.password = hash_password
        db.commit()
        db.refresh(user)
        return {"password": data.password, 'user': user}
    except JWTDecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Json Web Token invalid')
    except MissingTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='You be most have json web token')
    except AuthJWTException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Auth JWT Exception')


@router.put('/update/password/', status_code=status.HTTP_200_OK)
def update_password(data: schema.UpdatePassword, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
        phone_number = Authorize.get_jwt_subject()
        user = db.query(UserRestaurant).filter(UserRestaurant.phone_number == phone_number).first()
        old_password = data.password
        verifyPassword = verify_password(old_password, user.password)
        if verifyPassword:
            user.password = get_password_hash(data.new_password)
            db.commit()
            db.refresh(user)
            return {'detail': 'Password update'}
        return {'detail': 'Password be most mach'}
    except JWTDecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Json Web Token invalid')
    except MissingTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='You be most have json web token')
    except AuthJWTException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Auth JWT Exception')


@router.post('/send/')
def send_data(db: Session = Depends(get_db)):
    user = db.query(UserRestaurant).order_by(UserRestaurant.id.desc()).first()

    json_data = {'id': str(user.id), 'phone_number': str(user.phone_number), 'email': str(user.email),
                 'is_active': str(user.is_active),
                 'name': str(user.name), }
    re = requests.post('http://127.0.0.1:4500/get/user/res/', json=json_data)
    print(re)
    return 'OK'


@router.get("/get/data/user/{user_phone_number}/")
def test(user_phone_number: str, db: Session = Depends(get_db)):
    user = db.query(UserRestaurant).filter(UserRestaurant.phone_number == user_phone_number).first()
    if user:
        return user

# response: Response
# response.status_code = status.HTTP_201_CREATED
