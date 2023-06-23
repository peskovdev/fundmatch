from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.crud import handle_user
from app.db.main import get_db
from app.schemas.user import ConfirmCodeRequest, LoginRequest
from app.services.login_handler import handle_confirmation_code, send_sms


router = APIRouter(prefix="")


@router.post("/login", status_code=200)
def login(user: LoginRequest, db: Session = Depends(get_db)) -> dict:
    """
    1. Принимает на вход номер телефона
    2. Создает пользователя если его не существовало
    3. Генерируют одноразовый код входа
    4. Отправляет смс с кодом пользователю
    """
    handle_user(phone=user.phone, db=db)
    success_sms_result = send_sms(user.phone)

    if success_sms_result:
        return {"message": "SMS-Code was sent"}

    raise HTTPException(status_code=400, detail="SMS sending failed")


@router.post("/confirm-code", status_code=200)
def confirm_code(code: ConfirmCodeRequest, db: Session = Depends(get_db)) -> dict:
    """
    1. Принимает на вход код подтверждения
    2. При валидном коде высылает токен авторизации
    """

    code_confirmation_status, token = handle_confirmation_code(code.code)

    if code_confirmation_status is True:
        return {"token": token}
    else:
        raise HTTPException(status_code=400, detail="Confirmation code is invalid")
