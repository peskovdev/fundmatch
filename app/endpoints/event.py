from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.main import get_db
from app.schemas.event import EventCreateRequest, EventResponse
from app.schemas.login import Token
from app.services.event_manager import create_event, get_event_proc
from app.services.jwt_manager import get_token_payload


router = APIRouter(prefix="/event", tags=["Event"])


@router.post("/create")
def add_event(
    event_request: EventCreateRequest,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> EventResponse:
    """Health Check"""

    event = create_event(event_request, token_payload.id, db)

    return EventResponse.from_orm(event)


@router.get("/{event_id}")
def get_event(
    event_id: int,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> EventResponse:
    """Health Check"""

    event = get_event_proc(event_id, token_payload.id, db)

    return EventResponse.from_orm(event)
#
#
# @router.get("/{event_id}")
# def get_event(
#     event_id: int,
#     token_payload: Token = Depends(get_token_payload),
#     db: Session = Depends(get_db),
# ) -> EventResponse:
#     """Health Check"""
#
#     event = get_event_proc(event_id, token_payload.id, db)
#
#     return EventResponse.from_orm(event)
