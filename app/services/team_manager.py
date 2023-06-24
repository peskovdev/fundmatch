from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.crud import (
    add_member,
    create_team,
    get_team,
    get_user_by_id,
    get_user_by_phone,
    remove_member,
)
from app.db.models import Team
from app.schemas.team import TeamCreateRequest


def handle_team(team: TeamCreateRequest, creator_id: int, db: Session) -> Team:
    """Создаение команды"""

    user = get_user_by_id(creator_id, db)

    orm_team = create_team(team, user, db)

    return orm_team


def get_team_info(user_id: int, db: Session) -> Team:
    user = get_user_by_id(user_id, db)
    if len(user.teams) == 0:
        raise HTTPException(status_code=404, detail="User isn't a member of any team")
    team = user.teams.pop()
    return team


def get_team_info_by_team_id(team_id: int, user_id: int, db: Session) -> Team:
    team = get_team(team_id, db)
    user = get_user_by_id(user_id, db)
    if user not in team.members:
        raise HTTPException(status_code=401, detail="User is not a member of the team")

    return team


def add_team_member(member_phone: str, team_manager_id: int, db: Session) -> Team:
    new_member = get_user_by_phone(member_phone, db)

    team_manager = get_user_by_id(team_manager_id, db)
    team = get_team(team_manager.team_managed.id, db)
    if team is None:
        raise HTTPException(status_code=401, detail="User owning jwt-token is not a team manager")

    team = add_member(team, new_member, db)

    return team


def remove_team_member(member_id: int, team_manager_id: int, db: Session) -> Team:
    member = get_user_by_id(member_id, db)

    team_manager = get_user_by_id(team_manager_id, db)
    if team_manager.team_managed is None:
        raise HTTPException(status_code=401, detail="User owning jwt-token is not a team manager")

    team = get_team(team_manager.team_managed.id, db)

    if team is None:
        raise HTTPException(status_code=401, detail="User owning jwt-token has invalid team")

    if member not in team.members:
        raise HTTPException(status_code=400, detail="User is not a member of the team")

    team = remove_member(team, member, db)

    return team
