from pydantic import BaseModel


class Coupon(BaseModel):
    phone_number: str
