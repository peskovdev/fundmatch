from sqlalchemy.orm import Session

from app.db.models import Team
from app.schemas.team import TeamCreateRequest
from app.db.crud import create_team, get_user_by_id


def handle_team(team: TeamCreateRequest, creator_id: int, db: Session) -> Team:
    """Создаение команды"""

    user = get_user_by_id(creator_id, db)

    orm_team = create_team(team, user, db)

    return orm_team
