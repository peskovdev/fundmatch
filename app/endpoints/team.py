from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.main import get_db
from app.schemas.login import Token
from app.schemas.team import TeamCreateRequest, TeamCreateResponse, InviteRequest
from app.services.jwt_manager import get_token_payload
from app.services.team_manager import handle_team, get_team_info, add_team_member


router = APIRouter(prefix="/team")


@router.post("/create", status_code=200)
def create_team(
    team: TeamCreateRequest,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> TeamCreateResponse:
    """Создание команды"""

    orm_team = handle_team(team, token_payload.id, db)

    return TeamCreateResponse.from_orm(orm_team)


@router.get("/{team_id}", status_code=200)
def get_team(
    team_id: int,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> TeamCreateResponse:
    """Просмотр команды"""

    team = get_team_info(team_id, token_payload.id, db)

    return TeamCreateResponse.from_orm(team)


@router.post("/invite", status_code=200)
def invite_member(
    form_data: InviteRequest,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> TeamCreateResponse:
    """Пригласить участника в команду"""

    team = add_team_member(form_data.id, token_payload.id, db)

    return TeamCreateResponse.from_orm(team)
