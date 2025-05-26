from typing import TYPE_CHECKING

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import Accounts, Events, TicketTypes, Tickets
from ..core.exceptions import ValidationError, LoginAlreadyExistsException, InternalServerError
from ..core.config import GET_TABLE

if TYPE_CHECKING:
    from ..models.session import BaseModel
    from ..schemas import UserRegistrationResult, EventCreatedResult


async def user_registration(db: Session, name: str, login: str, password: str) -> 'UserRegistrationResult':
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

async def create_event(db: Session, creator_id: int, title: str, description: str, address: str) -> 'EventCreatedResult':
    """
    Функция для создания мероприятия

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        creator_id (int): ID создателя мероприятия.
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

async def search_user(db: Session, *, user_id: int | None = None, login: str | None = None) -> dict[str, Accounts | None]:
    """
    Возвращает Результат поиска пользователя.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        user_id (int): ID пользователя.
        login (str): Логин пользователя.

    Returns:
        dict[str, Accounts | None]: Вернет `None`, если элемент не найден, либо данные не указаны. Иначе - все данные пользователя в формате `{'id': user_info, 'login': user_info}`.
    """
    query = db.query(Accounts)

    result = {
        'id': query.filter(Accounts.id == user_id).first() if user_id is not None else None,
        'login': query.filter(Accounts.login == login).first() if login is not None else None
    }
    return result

async def all_info_table(db: Session, table_name: str) -> list:
    if not table_name:
        raise ValidationError()

    result = db.query(GET_TABLE[table_name]).all()
    return result