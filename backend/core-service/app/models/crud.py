from typing import TypedDict, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import Accounts, Events, TicketTypes, Tickets


class UserRegistrationResult(TypedDict):
    result: True
    user_id: Optional[int]
    error: Optional[str]

async def user_registration(db: Session, name: str, login: str, password: str) -> UserRegistrationResult:
    """
    Функция для регистрации аккаунта.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        login (str): Логин пользователя.
        password (str): Пароль пользователя (хеш).

    Returns:
        UserRegistrationResult (TypedDict). `{"result": True, "user_id": int}`

    Raises:
        UserRegistrationResult (TypedDict). `{"result": False, "error": "Причина ошибки"}`
    """
    # если один из параметров не указан
    if not db or not login or not password:
        return {'result': False, 'error': 'Укажите все данные'}

    try:
        new_user = Accounts(
            name=name,
            login=login,
            password_hash=password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {'result': True, 'user_id': new_user.id}
    except IntegrityError:
        return {'result': False, 'error': 'Аккаунт с таким логином/именем уже существует'}
    except Exception as e:
        return {'result': False, 'error': 'Ошибка сервера'}
        # raise HTTPException(status_code=500)


# async def is_exists_login(db: Session, login: str) -> bool:
#     """
#     Функция для проверки существует ли пользователь.

#     Args:
#         db (Session): Сессия SQLAlchemy для работы с БД.
#         login (str): Логин пользователя.

#     Returns:
#         bool: 
#             - При успехе: `{'result': True}`
#             - При ошибке: `{'result': False}`
#     """
#     if not Session or not login:
#         return {'result': False}

#     if db.query(Accounts).filter(Accounts.login == login).first():
#         return {'result': True}

#     return {'result': False}