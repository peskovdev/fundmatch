from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.crud import get_event, get_first_user_team, get_user_by_id, save_event
from app.db.models import Event
from app.schemas.event import EventCreateRequest


def create_event(event: EventCreateRequest, user_id: int, db: Session) -> Event:
    team = get_first_user_team(user_id, db)
    new_event = Event(
        title=event.title,
        team=team,
        goal=event.goal,
        address=event.address,
        event_time=event.event_time,
        notes=event.notes,
    )

    new_event = save_event(new_event, db)

    return new_event


def get_event_proc(event_id: int, user_id: int, db: Session) -> Event:
    user = get_user_by_id(user_id, db)
    event = get_event(event_id, db)
    if user not in event.participants:
        raise HTTPException(status_code=401, detail="User isn't participant of event")

    return event
