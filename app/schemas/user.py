from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    number: str
    name: str
