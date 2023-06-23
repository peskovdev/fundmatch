from typing import Optional


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


def handle_confirmation_code(code: str) -> tuple[bool, Optional[str]]:
    """Возвращает Токен Юзера"""
    ...
    if code == PLUGGED_CODE:
        return True, "token"
    return False, None
