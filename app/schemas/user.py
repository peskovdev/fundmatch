from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    phone: str = "+77771119999"
    full_name: Optional[str] = "John Doe"

    class Config:
        orm_mode = True
