"""Обработка запросов от базы данных"""

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import User


def get_user(user_id: int, db: Session) -> Optional[User]:
    """Пример функции"""
    user = db.get(User, user_id)
    return user
