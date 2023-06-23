from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.main import get_db
from app.db.models import User
from app.schemas.user import CreateUserRequest


router = APIRouter(prefix="")


@router.post("/create")
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)) -> tuple:
    """Принимает номер и имя"""
    new_user = User(phone=user.number, full_name=user.name)

    db.add(new_user)
    db.commit()

    return new_user, 200
