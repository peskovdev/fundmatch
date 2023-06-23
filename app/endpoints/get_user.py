from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.main import get_db
from app.db.models import User


router = APIRouter(prefix="")


@router.get("/get")
def get_user(db: Session = Depends(get_db)) -> tuple:
    """Возвращает список ползователей"""
    users = db.query(User).all()
    return users, 200
