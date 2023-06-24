from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.crud import create_team, get_team, get_user_by_id
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
