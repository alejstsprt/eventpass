from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from fastapi import Request, Response

from ..core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


async def set_jwt_cookie(response: Response, token: str):
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    response.set_cookie(
        key="jwt_token",
        value=token,
        httponly=True,
        expires=expiration_time,
        secure=False,  # secure=True, если используешь HTTPS
        samesite="lax",
        path="/"
    )

async def create_access_token(user_id: int) -> str:
    """
    Создание токена

    Args:
        int: user_id: Айди пользователя.

    Returns:
        str: Созданный токен: `токен`.
    """
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def token_verification(jwt_token) -> Optional[int]:
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
        if not user_id:
            return None
        return user_id
    except:
        return None


# curl.exe -X POST "http://192.168.0.107:8000/api/auth/exists-login" `
#   -H "accept: application/json" `
#   -H "Content-Type: application/json" `
#   --cookie "jwt_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0IiwiZXhwIjoxNzQ1MDA1NTAzfQ.-jAwn1XJvorfvtc5OrD_3pU4p40b7TH4dy6bVwKwpYk"