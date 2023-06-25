from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.crud import get_first_user_team, save_event
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
