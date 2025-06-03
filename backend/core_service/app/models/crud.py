"""
Костыльный модуль взаимодействия с бд без класса. позже нужно сделать как класс и сократить количество функций
"""

from typing import TYPE_CHECKING, Any, Dict, Literal, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..core.config import config
from ..core.exceptions import (
    InternalServerError,
    LoginAlreadyExistsException,
    TicketTypeError,
    ValidationError,
)
from ..core.logger import logger_api
from .models import Accounts, Events, Tickets, TicketTypes

if TYPE_CHECKING:
    from ..schemas import (
        EditEvent,
        EventCreatedResult,
        IntEventCreatorId,
        IntUserId,
        StrEventAddress,
        StrEventDescription,
        StrEventTitle,
        StrUserLogin,
        StrUserName,
        StrUserPassword,
        UserRegistrationResult,
    )
    from .session import BaseModel


async def user_registration(
    db: Session, name: "StrUserName", login: "StrUserLogin", password: "StrUserPassword"
) -> "UserRegistrationResult":
    """
    Функция для регистрации аккаунта.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        name (StrUserName): Имя пользователя.
        login (StrUserLogin): Логин пользователя.
        password (StrUserPassword): Пароль пользователя (хеш).

    Returns:
        UserRegistrationResult (TypedDict): `{'result': True, 'user_id': int}`

    Raises:
        ValidationError (HTTPException): Неверные входные данные.
        LoginAlreadyExistsException (HTTPException): Имя/Логин уже занят.
        InternalServerError (HTTPException): Ошибка сервера.
    """
    # if not db or not login or not password:
    #     logger_api.error(f'Неправильно переданы данные. {db = }, {login = }, {password = }')
    #     raise ValidationError()

    try:
        new_user = Accounts(
            name=name,
            login=login,
            password_hash=password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"result": True, "user_id": new_user.id}
    except IntegrityError:
        logger_api.error("Имя/Логин уже занят")
        raise LoginAlreadyExistsException()
    except Exception as e:
        logger_api.exception(f"Внутренняя ошибка сервера. Проблемы с сейвом БД: {e}")
        raise InternalServerError()


async def create_type_ticket_event(
    db: Session,
    event_id: int,
    ticket_type: Literal["Vip", "Standard", "Econom"],
    description: str,
    price: int,
    total_count: int,
) -> ...:
    """
    Функция для создания типа билета для мероприятия.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        event_id (int): ID мероприятия для которого создаем тип билета.
        ticket_type (Literal["Vip", "Standard", "Econom"]): Тип билета.
        description (str): Описание типа билета мероприятия.
        price (int): Цена данного типа билета мероприятия.
        total_count (int): Стоимость данного типа белета мероприятия.

    Returns:
        ... (TypedDict):
        ```
        {
        "result": True,
            "event": {
                "id": new_type_ticket_event.id,
                "event_id": new_type_ticket_event.event_id,
                "ticket_type": new_type_ticket_event.type,
                "description": new_type_ticket_event.description,
                "price": new_type_ticket_event.price,
                "total_count": new_type_ticket_event.total_count
            },
        }
        ```

    Raises:
        ValidationError: _description_
        InternalServerError: _description_
    """
    if ticket_type not in config.TYPE_TICKETS:
        logger_api.error(f"Неправильный тип мероприятия {ticket_type = }")
        raise ValidationError()

    existing_ticket = (
        db.query(TicketTypes)
        .filter(TicketTypes.event_id == event_id, TicketTypes.type == ticket_type)
        .first()
    )

    if existing_ticket:
        logger_api.error(
            f"Данный тип билета для этого мероприятия уже существует {ticket_type = }"
        )
        raise TicketTypeError()

    try:
        new_type_ticket_event = TicketTypes(
            event_id=event_id,
            type=ticket_type,
            description=description,
            price=price,
            total_count=total_count,
        )
        db.add(new_type_ticket_event)
        db.commit()
        db.refresh(new_type_ticket_event)

        return {
            "result": True,
            "event": {
                "id": new_type_ticket_event.id,
                "event_id": new_type_ticket_event.event_id,
                "ticket_type": new_type_ticket_event.type,
                "description": new_type_ticket_event.description,
                "price": new_type_ticket_event.price,
                "total_count": new_type_ticket_event.total_count,
            },
        }
    except Exception as e:
        logger_api.exception(f"Внутренняя ошибка сервера. Проблемы с сейвом БД: {e}")
        raise InternalServerError()


async def create_event(
    db: Session,
    creator_id: "IntEventCreatorId",
    status: Literal["опубликовано", "завершено", "черновик"],
    title: "StrEventTitle",
    description: "StrEventDescription",
    address: "StrEventAddress",
) -> "EventCreatedResult":
    """
    Функция для создания мероприятия

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        creator_id (IntEventCreatorId): ID создателя мероприятия.
        status (Literal['опубликовано', 'завершено', 'черновик']): Статус мероприятия.
        title (StrEventTitle): Название мероприятия.
        description (StrEventDescription): Описание мероприятия.
        address (StrEventAddress): Адрес мероприятия.

    Returns:
        EventCreatedResult (TypedDict):
        ```
        {
            'result': True,
            'event': {
                'id': id,
                'status': status,
                'creator_id': creator_id,
                'title': title,
                'description': description,
                'address': address,
                'time_create': datetime
            }
        }
        ```

    Raises:
        ValidationError (HTTPException): Неверные входные данные.
        InternalServerError (HTTPException): Ошибка сервера.
    """
    # if not db or not creator_id or not status or not title or not description or not address:
    #     logger_api.error(f'Неправильно переданы данные. {db = }, {creator_id = }, {status = }, {title = }, {description = }, {address = }')
    #     raise ValidationError()

    if status not in config.STATUS_EVENTS:
        logger_api.error(f"Неправильно статус мероприятия {status = }")
        raise ValidationError()

    try:
        new_event = Events(
            creator_id=creator_id,
            status=status,
            title=title,
            description=description,
            address=address,
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        return {
            "result": True,
            "event": {
                "id": new_event.id,
                "status": new_event.status,
                "creator_id": new_event.creator_id,
                "title": new_event.title,
                "description": new_event.description,
                "address": new_event.address,
                "time_create": new_event.datetime,
            },
        }
    except Exception as e:
        logger_api.exception(f"Внутренняя ошибка сервера. Проблемы с сейвом БД: {e}")
        raise InternalServerError()


async def search_user(
    db: Session,
    *,
    user_id: Optional["IntUserId"] = None,
    login: Optional["StrUserLogin"] = None,
) -> dict[str, Accounts | None]:
    """
    Возвращает Результат поиска пользователя.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        user_id (IntUserId): ID пользователя.
        login (StrUserLogin): Логин пользователя.

    Returns:
        dict[str, Accounts | None]: Вернет `None`, если элемент не найден, либо данные не указаны. Иначе - все данные пользователя в формате `{'id': user_info, 'login': user_info}`.
    """
    query = db.query(Accounts)

    result = {
        "id": (
            query.filter(Accounts.id == user_id).first()
            if user_id is not None
            else None
        ),
        "login": (
            query.filter(Accounts.login == login).first() if login is not None else None
        ),
    }
    return result


async def all_info_table(
    db: Session, table_name: Literal["Accounts", "Events", "TicketTypes", "Tickets"]
) -> list["BaseModel"]:
    """
    Функция для возврата всех данных таблицы.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        table_name (Literal['Accounts', 'Events', 'TicketTypes', 'Tickets']): Название таблицы.

    Returns:
        (list[str, Any]): Все данные таблицы.

    Raises:
        ValidationError: Неправильные данные.
    """
    if table_name not in config.GET_TABLE:
        text_error = f"Неправильно переданы данные. {db = }, {table_name = }"
        raise ValueError(text_error)

    result = db.query(config.GET_TABLE[table_name]).all()
    return result


# TODO: event_id, EditEvent заменить на другое, ведь функция для всех таблиц
async def edit_info(
    db: Session,
    table_name: Literal["Accounts", "Events", "TicketTypes", "Tickets"],
    event_id: int,
    data: "EditEvent",
) -> "BaseModel":
    """
    Редактирование информации в таблицах db.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        table_name (Literal['Accounts', 'Events', 'TicketTypes', 'Tickets']): Название таблицы.
        id (int): Айди мероприятия.
        data (EditEvent): Данные которые нужно изменить.

    Returns:
        (list[Dict[str, Any]]): Вся информация об измененном обьекте.

    Raises:
        ValueError: Неправильноe название таблицы.
        ValidationError: Неверные данные.
    """
    if table_name not in config.GET_TABLE:
        text_error = f"Неправильно переданы данные. {db = }, {table_name = }"
        raise ValueError(text_error)

    if not data.model_dump(exclude_unset=True):
        raise ValidationError()

    event = db.query(config.GET_TABLE[table_name]).filter_by(id=event_id).first()
    if not event:
        raise ValidationError()

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event
