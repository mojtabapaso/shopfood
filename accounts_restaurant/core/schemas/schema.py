from pydantic import BaseModel


class PhoneNumber(BaseModel):
    phone_number: str


class OtpCode(BaseModel):
    code: int
    phone_number: str


class UserRestaurant(BaseModel):
    phone_number: str
    email: str
    name: str


class UserRestaurantPassword(BaseModel):
    password: str


class loginPassword(PhoneNumber, UserRestaurantPassword):
    pass


class SetPassword(UserRestaurantPassword):
    password2: str


class UpdatePassword(UserRestaurantPassword):
    new_password: str
