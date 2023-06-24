"""Обработка запросов от базы данных"""

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import User


def handle_user(phone: str, db: Session) -> None:
    """Проверяет существует ли пользователь, если нет то добавляет"""

    user = db.query(User).filter(User.phone == phone).first()
    if user is None:
        create_user(phone, db)


def create_user(phone: str, db: Session) -> None:
    user = User(phone=phone)
    db.add(user)
    db.commit()


def get_user_by_phone(phone: str, db: Session) -> Optional[User]:
    user = db.query(User).filter(User.phone == phone).first()
    if user is None:
        return None
    return user


def get_user_by_id(id: int, db: Session) -> Optional[User]:
    user = db.get(User, id)
    return user
