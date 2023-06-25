from app.schemas.user import UserResponse
from app.db.enums import EventStatus

from pydantic import BaseModel


class EventCreateRequest(BaseModel):
    title: str = "Football 23.05.2023"
    goal: float = 75000.0
    address: str = "Алалыкина 11"
    event_time: str = "23/05/2023"
    notes: str = "Взять тормозки"


class ContributionRequest(BaseModel):
    user_id: int
    event_id: int


class ContributionResponse(BaseModel):
    id: int
    user: UserResponse
    amount: float

    class Config:
        orm_mode = True


class EventSubResponse(BaseModel):
    id: int
    title: str = "Football 23.05.2023"
    goal: float
    current_amount: float
    status: EventStatus

    class Config:
        orm_mode = True


class EventResponse(BaseModel):
    id: int
    title: str = "Football 23.05.2023"
    team_id: int
    participants: list[UserResponse]
    contributions: list[ContributionResponse]
    goal: float
    current_amount: float
    status: EventStatus

    class Config:
        orm_mode = True


class ChangeUsernameRequest(BaseModel):
    full_name: str = "John Doe"
