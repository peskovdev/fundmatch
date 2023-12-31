from typing import Any

import jwt
from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from app.config import settings
from app.db.crud import get_user_by_phone
from app.db.models import User
from app.schemas.login import Token


def get_token_payload(token: str = Security(APIKeyHeader(name="Authorization"))) -> Token:
    """Validates token and returns decoded Token"""
    try:
        if token[-1] == '"':
            token = token[:-1]
        if token[0] == '"':
            token = token[1:]

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("id") is None:
            raise HTTPException(status_code=400, detail="Invalid token: missing id")
        decoded_token = Token(
            id=payload.get("id"),
            full_name=str(payload.get("full_name")),
            phone=payload.get("phone"),
        )
        return decoded_token
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def create_token(phone: str, db: Session) -> str:
    user = get_user_by_phone(phone, db)

    token_data = _generate_a_token(user)
    encoded_jwt = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def _generate_a_token(user: User) -> dict[str, Any]:
    payload = {
        "id": user.id,
        "full_name": user.full_name,
        "phone": user.phone,
    }
    return payload
