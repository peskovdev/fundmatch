from pydantic import BaseModel

from .user import UserResponse


class TeamCreateRequest(BaseModel):
    name: str = "Navi"


class TeamCreateResponse(BaseModel):
    id: str
    name: str = "Navi"
    manager: UserResponse
    members: list[UserResponse]

    class Config:
        orm_mode = True


class TeamMemberRequest(BaseModel):
    id: int
