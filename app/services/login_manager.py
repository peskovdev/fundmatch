from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.jwt_manager import create_token


PLUGGED_CODE = "491341"


def send_sms(phone: str) -> bool:
    """Возвращает результат отправки (успех/крах)
    Здесь должна быть имплементирована логика генерации токена,
    сохранения его в редисе, и непосредственно отправка письма
    """
    ...
    if True:
        return True
    return False


def handle_confirmation_code(code: str, phone: str, db: Session) -> str:
    """Возвращает Токен Юзера"""
    ...
    if code == PLUGGED_CODE:
        token = create_token(phone, db)
        return token
    raise HTTPException(status_code=400, detail="Confirmation code is invalid")
