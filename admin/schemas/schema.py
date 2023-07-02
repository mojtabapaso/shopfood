from pydantic import BaseModel


class AdminLogin(BaseModel):
    phone_number: str


