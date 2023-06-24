from pydantic import BaseModel


class LoginRequest(BaseModel):
    phone: str = "+77771119999"


class ConfirmCodeRequest(BaseModel):
    code: str = "491341"
    phone: str = "+77771119999"
