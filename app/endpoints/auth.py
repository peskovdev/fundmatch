from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.crud import get_user_by_id, get_user_by_phone, handle_user, update_username
from app.db.main import get_db
from app.schemas.login import ConfirmCodeRequest, LoginRequest, Token
from app.schemas.user import UserResponse, ChangeUsernameRequest
from app.services.jwt_manager import get_token_payload
from app.services.login_manager import handle_confirmation_code, send_sms


router = APIRouter(prefix="/auth", tags=["Auth"])


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

    token = handle_confirmation_code(code.code, code.phone, db)

    return {"token": token}


@router.patch("/change-username", status_code=200)
def change_username(
    form_data: ChangeUsernameRequest,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> UserResponse:

    user = update_username(token_payload.id, form_data.full_name, db)

    return UserResponse.from_orm(user)


@router.get("/get-credentials", status_code=200)
def get_credentials(
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> UserResponse:
    """Ручка принимает токен в заголовках и возвращает данные пользователя"""

    user = get_user_by_id(token_payload.id, db)

    return UserResponse.from_orm(user)


@router.get("/get-user", status_code=200)
def get_user(
    phone: str,
    token_payload: Token = Depends(get_token_payload),
    db: Session = Depends(get_db),
) -> UserResponse:
    """Возвращает информацию о пользователе по номеру"""

    user = get_user_by_phone(phone, db)

    return UserResponse.from_orm(user)
