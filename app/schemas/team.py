from pydantic import BaseModel

from .user import UserResponse


class TeamCreateRequest(BaseModel):
    name: str = "Navi"


class TeamResponse(BaseModel):
    id: str
    name: str = "Navi"
    manager: UserResponse
    members: list[UserResponse]

    class Config:
        orm_mode = True


class TeamInviteMemberRequest(BaseModel):
    phone: str = "+77771119999"


class TeamMemberRequest(BaseModel):
    id: int
