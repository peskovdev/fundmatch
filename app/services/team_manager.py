from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.crud import add_member, create_team, get_team, get_user_by_id
from app.db.models import Team
from app.schemas.team import TeamCreateRequest


def handle_team(team: TeamCreateRequest, creator_id: int, db: Session) -> Team:
    """Создаение команды"""

    user = get_user_by_id(creator_id, db)

    orm_team = create_team(team, user, db)

    return orm_team


def get_team_info(team_id: int, user_id: int, db: Session) -> Team:
    team = get_team(team_id, db)
    user = get_user_by_id(user_id, db)
    if user not in team.members:
        raise HTTPException(status_code=401, detail="This user aren't member of the team")

    return team


def add_team_member(new_member_id: int, team_manager_id: int, db: Session) -> Team:
    new_member = get_user_by_id(new_member_id, db)

    team_manager = get_user_by_id(team_manager_id, db)
    team = get_team(team_manager.team_managed.id, db)
    if team is None:
        raise HTTPException(status_code=401, detail="This user is not a team manager")

    add_member(team, new_member, db)

    return team
