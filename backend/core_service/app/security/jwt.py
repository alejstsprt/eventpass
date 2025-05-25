from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from fastapi import Request, Response
from sqlalchemy import Column

from ..core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


async def set_jwt_cookie(response: Response, token: str) -> None:
    expires = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(days=30)

    response.set_cookie(
        key="jwt_token",
        value=token,
        httponly=True,
        expires=expires,
        secure=False,  # secure=True, если используешь HTTPS
        samesite="lax",
        path="/"
    )

async def create_access_token(user_id: int | Column[int]) -> str:
    """
    Создание токена

    Args:
        int/Column[int]: user_id: Айди пользователя.

    Returns:
        str: Созданный токен: `токен`.
    """
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expires  # Время истечения в UTC
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def token_verification(jwt_token: str) -> Optional[int]:
    """
    Для проверки токена + получения айди пользователя.

    Args:
        request: Токен

    Returns:
        str: ID пользователя (subject из токена).

    Raises:
        NoneType: None
    """
    if not jwt_token:
        return None

    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return int(user_id) if user_id else None
    except (JWTError, ValueError):
        return None


# curl.exe -X POST "http://192.168.0.107:8000/api/auth/exists-login" `
#   -H "accept: application/json" `
#   -H "Content-Type: application/json" `
#   --cookie "jwt_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzQ1MDA1NTAzfQ.-jAwn1XJvorfvtc5OrD_3pU4p40b7TH4dy6bVwKwpYk"