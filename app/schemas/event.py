from app.schemas.user import UserResponse
from app.db.enums import EventStatus

from pydantic import BaseModel


class EventCreateRequest(BaseModel):
    title: str = "Football 23.05.2023"
    goal: float = 75000.0
    address: str = "Алалыкина 11"
    event_time: str = "23.05.2023 16:30"
    notes: str = "Взять тормозки"


class EventSubResponse(BaseModel):
    id: int
    title: str = "Football 23.05.2023"
    goal: float
    status: EventStatus

    class Config:
        orm_mode = True


class EventResponse(BaseModel):
    id: int
    title: str = "Football 23.05.2023"
    team_id: int
    participants: list[UserResponse]
    goal: float
    status: EventStatus

    class Config:
        orm_mode = True


class ChangeUsernameRequest(BaseModel):
    full_name: str = "John Doe"
