from typing import TypedDict, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import Accounts, Events, TicketTypes, Tickets
from ..security.hashing import hash_password


class form_user_registration(TypedDict, total=False):
    result: True
    user_id: Optional[int]
    error: Optional[str]

async def user_registration(db: Session, login: str, password: str) -> form_user_registration: #Dict[str, Union[bool, int, str]]:
    """
    Функция для регистрации аккаунта.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        login (str): Логин пользователя.
        password (str): Пароль пользователя.

    Returns:
        form_user_registration:
            - При успехе: `{"result": True, "user_id": int}`
            - При ошибке: `{"result": False, "error": "Причина ошибки"}`
    """
    # если один из параметров не указан
    if not db or not login or not password:
        return {'result': False, 'error': 'Укажите все данные'}

    try:
        new_user = Accounts(
            login=login,
            password_hash=hash_password(password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {'result': True, 'user_id': new_user.id}
    except IntegrityError:
        return {'result': False, 'error': 'Аккаунт уже существует'}
    except Exception as e:
        return {'result': False, 'error': 'Ошибка сервера'}

async def is_exists_login(db: Session, login: str) -> bool:
    """
    Функция для проверки существует ли пользователь.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        login (str): Логин пользователя.

    Returns:
        bool: 
            - При успехе: `{'result': True}`
            - При ошибке: `{'result': False}`
    """
    if not Session or not login:
        return {'result': False}

    if db.query(Accounts).filter(Accounts.login == login).first():
        return {'result': True}

    return {'result': False}