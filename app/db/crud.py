"""Обработка запросов от базы данных"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Team, User, Event
from app.schemas.team import TeamCreateRequest


def handle_user(phone: str, db: Session) -> None:
    """Проверяет существует ли пользователь, если нет то добавляет"""

    user = db.query(User).filter(User.phone == phone).first()
    if user is None:
        create_user(phone, db)


def create_user(phone: str, db: Session) -> None:
    user = User(phone=phone)
    db.add(user)
    db.commit()


def get_user_by_phone(phone: str, db: Session) -> User:
    user = db.query(User).filter(User.phone == phone).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User doesn't exist")
    return user


def get_user_by_id(id: int, db: Session) -> User:
    user = db.get(User, id)
    if user is None:
        raise HTTPException(status_code=400, detail="User doesn't exist")

    return user


def update_username(user_id: int, full_name: str, db: Session) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=400, detail="User doesn't exist")

    user.full_name = full_name
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_team(team: TeamCreateRequest, user: User, db: Session) -> Team:
    if user.team_managed is not None:
        raise HTTPException(status_code=400, detail="User is already managing a team")

    orm_team = Team(
        name=team.name,
        manager=user,
        members=[user],
    )
    db.add(orm_team)
    db.commit()
    db.refresh(orm_team)
    return orm_team


def get_team(id: int, db: Session) -> Team:
    team = db.get(Team, id)
    if team is None:
        raise HTTPException(status_code=400, detail="Team doesn't exist")

    return team


def get_first_user_team(user_id: int, db: Session) -> Team:
    team = db.query(Team).join(User.teams).filter(User.id == user_id).first()

    if team is None:
        raise HTTPException(status_code=400, detail="User isn't a member of any team")

    return team


def add_member(team: Team, new_member: User, db: Session) -> Team:
    team.members.append(new_member)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def remove_member(team: Team, member: User, db: Session) -> Team:
    team.members.remove(member)
    db.commit()
    db.refresh(team)
    return team


def save_event(event: Event, db: Session) -> Event:
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_event(id: int, db: Session) -> Event:
    event = db.get(Event, id)
    if event is None:
        raise HTTPException(status_code=400, detail="Event doesn't exist")

    return event
