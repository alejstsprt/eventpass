from typing import TypedDict, Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import Accounts, Events
from ..core.exceptions import ValidationError, LoginAlreadyExistsException, InternalServerError


class UserRegistrationResult(TypedDict):
    result: True
    user_id: Optional[int]
    error: Optional[str]

class EventDetails(TypedDict):
    id: int
    creator_id: int
    title: str
    description: str
    address: str
    time_create: DateTime

class EventCreatedResult(TypedDict):
    result: True
    event: EventDetails


async def user_registration(db: Session, name: str, login: str, password: str) -> UserRegistrationResult:
    """
    Функция для регистрации аккаунта.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        login (str): Логин пользователя.
        password (str): Пароль пользователя (хеш).

    Returns:
        UserRegistrationResult (TypedDict): `{'result': True, 'user_id': int}`

    Raises:
        ValidationError (HTTPException): Неверные входные данные.
        LoginAlreadyExistsException (HTTPException): Имя/Логин уже занят.
        InternalServerError (HTTPException): Ошибка сервера.
    """
    # если один из параметров не указан
    if not db or not login or not password:
        raise ValidationError()

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
        raise LoginAlreadyExistsException()
    except Exception as e:
        raise InternalServerError()

async def create_event(db: Session, creator_id: str, title: str, description: str, address: str) -> EventCreatedResult:
    """
    Функция для создания мероприятия

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        creator_id (str): ID создателя мероприятия.
        title (str): Название мероприятия.
        description (str): Описание мероприятия.
        address (str): Адрес мероприятия.

    Returns:
        EventCreatedResult (TypedDict): `{
            'result': True,
            'event': {
                'id': id,
                'creator_id': creator_id,
                'title': title,
                'description': description,
                'address': address,
                'time_create': datetime
            }
        }`

    Raises:
        ValidationError (HTTPException): Неверные входные данные.
        InternalServerError (HTTPException): Ошибка сервера.
    """
    if not db or not creator_id or not title or not description or not address:
        raise ValidationError()

    try:
        new_event = Events(
            creator_id=creator_id,
            title=title,
            description=description,
            address=address
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        return {
            'result': True,
            'event': {
                'id': new_event.id,
                'creator_id': new_event.creator_id,
                'title': new_event.title,
                'description': new_event.description,
                'address': new_event.address,
                'time_create': new_event.datetime
            }
        }
    except Exception as e:
        raise InternalServerError()