from pydantic import BaseModel


class LoginRequest(BaseModel):
    phone: str


class ConfirmCodeRequest(BaseModel):
    code: str
    phone: str
