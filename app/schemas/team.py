from pydantic import BaseModel

from app.schemas.user import UserResponse
from app.schemas.event import EventSubResponse


class TeamCreateRequest(BaseModel):
    name: str = "Navi"


class TeamResponse(BaseModel):
    id: str
    name: str = "Navi"
    manager: UserResponse
    members: list[UserResponse]
    events: list[EventSubResponse]
    count_members: int
    count_events: int

    class Config:
        orm_mode = True


class TeamInviteMemberRequest(BaseModel):
    phone: str = "+77771119999"


class TeamMemberRequest(BaseModel):
    id: int
