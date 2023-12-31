from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.main import get_db
from app.schemas.login import Token
from app.schemas.team import (
    TeamCreateRequest,
    TeamInviteMemberRequest,
    TeamMemberRequest,
    TeamResponse,
)
from app.services.jwt_manager import get_token_payload
from app.services.team_manager import (
    add_team_member,
    get_team_info_by_team_id,
    handle_team,
    remove_team_member,
)

from app.db.crud import get_first_user_team

router = APIRouter(prefix="/team", tags=["Team"])


@router.post("/create", status_code=200)
def create_team(
    team: TeamCreateRequest,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> TeamResponse:
    """Создание команды"""

    orm_team = handle_team(team, token_payload.id, db)

    return TeamResponse.from_orm(orm_team)


@router.get("", status_code=200)
def get_team(
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> TeamResponse:
    """Получить свою команду"""

    team = get_first_user_team(token_payload.id, db)

    return TeamResponse.from_orm(team)


@router.get("/{team_id}", status_code=200)
def get_team_by_id(
    team_id: int,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> TeamResponse:
    """Просмотр команды"""

    team = get_team_info_by_team_id(team_id, token_payload.id, db)

    return TeamResponse.from_orm(team)


@router.post("/invite", status_code=200)
def invite_member(
    form_data: TeamInviteMemberRequest,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> TeamResponse:
    """Пригласить участника в команду"""

    team = add_team_member(form_data.phone, token_payload.id, db)

    return TeamResponse.from_orm(team)


@router.delete("/remove-member", status_code=200)
def remove_member(
    form_data: TeamMemberRequest,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> TeamResponse:
    """Удалить члена команды"""

    team = remove_team_member(form_data.id, token_payload.id, db)

    return TeamResponse.from_orm(team)
