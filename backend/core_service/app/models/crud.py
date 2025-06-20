"""
Костыльный модуль взаимодействия с бд без класса. позже нужно сделать как класс и сократить количество функций
"""

from collections import defaultdict
from typing import TYPE_CHECKING, Literal, Optional, TypeVar

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from core.config import config
from core.exceptions import (
    ForbiddenError,
    ForbiddenUserError,
    InternalServerError,
    LoginAlreadyExistsException,
    NameAlreadyExistsException,
    TicketLimitError,
    TicketTypeError,
    ValidationError,
)
from core.logger import logger_api
from models.models import Accounts, Events, Tickets, TicketTypes
from models.session import DBBaseModel

if TYPE_CHECKING:
    from pydantic import BaseModel

    from schemas import (
        ActivateQrCodeResult,
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

T = TypeVar("T", bound=DBBaseModel)


async def user_registration(
    db: Session, name: "StrUserName", login: "StrUserLogin", password: "StrUserPassword"
) -> "Accounts":
    """
    Функция для регистрации аккаунта.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        name (StrUserName): Имя пользователя.
        login (StrUserLogin): Логин пользователя.
        password (StrUserPassword): Пароль пользователя (хеш).

    Returns:
        Accounts (DBBaseModel): Всю информацию о пользователе.

    Raises:
        ValidationError (HTTPException): Неверные входные данные.
        LoginAlreadyExistsException (HTTPException): Логин уже занят.
        NameAlreadyExistsException (HTTPException): Имя уже занято.
        InternalServerError (HTTPException): Ошибка сервера.
    """
    try:
        new_user = Accounts(
            name=name,
            login=login,
            password_hash=password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        if "users.login" in str(e).split():  # HACK: костыль
            logger_api.error("Логин уже занят")
            raise LoginAlreadyExistsException()
        else:
            logger_api.error("Имя уже занято")
            raise NameAlreadyExistsException()


async def create_ticket_event(
    db: Session, event_id: int, user_id: int, ticket_type_id: int, unique_code: str
) -> Tickets | None:
    """
    Создание билета на мероприятие.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        event_id (int): ID мероприятия.
        user_id (int): ID создателя.
        ticket_type_id (int): ID типа билета.
        unique_code (str): hmac код билета.

    Returns:
        Tickets: Информацию о билете, пользователе, типе билета и мероприятии.

    Raises:
        InternalServerError: Ошибка сервера.
    """
    if not (db.query(Events).filter(Events.id == event_id).first()):
        logger_api.error(f"Данного мероприятия c {event_id = } не существует")
        raise ValidationError()

    ticket_type = db.query(TicketTypes).filter(TicketTypes.id == ticket_type_id).first()
    if not ticket_type:
        logger_api.error(f"Данного типа билета c {ticket_type_id = } не существует")
        raise ValidationError()

    count = (
        db.query(func.count(Tickets.id))
        .filter(Tickets.ticket_type_id == ticket_type.id)
        .scalar()
    )
    if ticket_type.total_count <= count:
        raise TicketLimitError()

    try:
        new_ticket = Tickets(
            event_id=event_id,
            user_id=user_id,
            ticket_type_id=ticket_type_id,
            unique_code=unique_code,
        )
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

        ticket_with_details = (
            db.query(Tickets)
            .options(
                joinedload(Tickets.event),
                joinedload(Tickets.user),
                joinedload(Tickets.ticket_type),
            )
            .filter(Tickets.id == new_ticket.id)
            .first()
        )
        return ticket_with_details
    except Exception as e:
        db.rollback()
        logger_api.exception(f"Внутренняя ошибка сервера. Проблемы с сейвом БД: {e}")
        raise InternalServerError()


async def create_type_ticket_event(
    db: Session,
    event_id: int,
    ticket_type: Literal["Vip", "Standard", "Econom"],
    description: str,
    price: int,
    total_count: int,
) -> "TicketTypes":
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
        TicketTypes (DBBaseModel): Всю информацию о созданном типе билета мероприятия.

    Raises:
        ValidationError: Неверные данные.
        TicketTypeError: Данный тип билета для этого мероприяия уже существует.
        InternalServerError: Ошибка сервера.
    """
    if ticket_type not in config.TYPE_TICKETS:
        logger_api.error(f"Неправильный тип мероприятия {ticket_type = }")
        raise ValidationError()

    existing_ticket = (
        db.query(TicketTypes)
        .filter(
            TicketTypes.event_id
            == event_id,  # находит все существующие типы этого мероприятия
            TicketTypes.type == ticket_type,  # и смотрит есть ли такой тип уже
        )
        .first()
    )

    if existing_ticket:
        logger_api.error(
            f"Данный тип билета для этого мероприяия уже существует {ticket_type = }"
        )
        raise TicketTypeError()

    event = (
        db.query(Events)
        .filter(
            Events.id == event_id,
        )
        .first()
    )
    if not event:
        logger_api.error(f"Мероприятие под {event_id = } не существует")
        raise ValidationError()

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

        return new_type_ticket_event
    except Exception as e:
        db.rollback()
        logger_api.exception(f"Внутренняя ошибка сервера. Проблемы с сейвом БД: {e}")
        raise InternalServerError()


async def create_event(
    db: Session,
    creator_id: "IntEventCreatorId",
    status: Literal["опубликовано", "завершено", "черновик"],
    title: "StrEventTitle",
    category: Literal[
        "Концерт", "Фестиваль", "Конференция", "Выставка", "Спорт", "Театр", "Другое"
    ],
    description: "StrEventDescription",
    address: "StrEventAddress",
) -> "Events":
    """
    Функция для создания мероприятия

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        creator_id (IntEventCreatorId): ID создателя мероприятия.
        status (Literal[...]): Статус мероприятия.
        title (StrEventTitle): Название мероприятия.
        category (Literal[...]): Категория мероприятия.
        description (StrEventDescription): Описание мероприятия.
        address (StrEventAddress): Адрес мероприятия.

    Returns:
        Events (DBBaseModel): Всю информацию о созданном мероприятии.

    Raises:
        ValidationError (HTTPException): Неверные входные данные.
        InternalServerError (HTTPException): Ошибка сервера.
    """
    if status not in config.STATUS_EVENTS:
        logger_api.error(f"Неправильно статус мероприятия {status = }")
        raise ValidationError()

    if category not in config.CATEGORY_EVENTS:
        logger_api.error(f"Неправильно статус мероприятия {status = }")
        raise ValidationError()

    try:
        new_event = Events(
            creator_id=creator_id,
            status=status,
            title=title,
            category=category,
            description=description,
            address=address,
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)

        return new_event
    except Exception as e:
        db.rollback()
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
) -> list["DBBaseModel"]:
    """
    Функция для возврата всех данных таблицы.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        table_name (Literal['Accounts', 'Events', 'TicketTypes', 'Tickets']): Название таблицы.

    Returns:
        (list[str, Any]): Все данные таблицы.

    Raises:
        ValidationError (HTTPException): Неправильные данные.
    """
    if table_name not in config.GET_TABLE:
        text_error = f"Неправильно переданы данные. {db = }, {table_name = }"
        raise ValueError(text_error)

    result = db.query(config.GET_TABLE[table_name]).all()
    return result


async def get_types_ticket_event(db: Session, event_id: int) -> list["TicketTypes"]:
    """
    Возвращает типы билета мероприятия.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        event_id (int): ID мероприятия.

    Returns:
        list[DBBaseModel]: Результат поиска.
    """
    return db.query(TicketTypes).filter(TicketTypes.event_id == event_id).all()


async def edit_data(
    db: Session,
    table_name: Literal["Accounts", "Events", "TicketTypes", "Tickets"],
    id: int,
    data: "BaseModel",
) -> "DBBaseModel":
    """
    Редактирование информации в таблицах db.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        table_name (Literal['Accounts', 'Events', 'TicketTypes', 'Tickets']): Название таблицы.
        id (int): Айди нужного элемента для изменения.
        data (T): Данные которые нужно изменить.

    Returns:
        T (BaseModel): Вся информация об измененном обьекте.

    Raises:
        ValueError (Exception): Неправильноe название таблицы.
        ValidationError (HTTPException): Неверные данные.
    """
    if table_name not in config.GET_TABLE:
        text_error = f"Неправильно переданы данные. {db = }, {table_name = }"
        raise ValueError(text_error)

    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        raise ValidationError()

    obj = db.query(config.GET_TABLE[table_name]).filter_by(id=id).first()
    if not obj:
        raise ValidationError()

    for field, value in update_data.items():
        setattr(obj, field, value)

    db.commit()
    db.refresh(obj)
    return obj


async def del_event(
    db: Session,
    event_id: int,
    user_id: int,
) -> None:
    """
    Удаление мероприятия вместе с типами и билетами.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        event_id (int): ID мероприятия.
        user_id (int): ID пользователя.

    Raises:
        ValidationError: Неверные данные.
        ForbiddenUserError: Отказано в доступе.
        InternalServerError: Ошибка сервера.
    """
    event = db.query(Events).get(event_id)
    if not event:
        raise ValidationError()
    if event.creator_id != user_id:
        raise ForbiddenUserError()

    try:
        db.query(Tickets).filter(
            Tickets.ticket_type_id.in_(
                db.query(TicketTypes.id).filter(TicketTypes.event_id == event_id)
            )
        ).delete(synchronize_session=False)

        db.query(TicketTypes).filter(TicketTypes.event_id == event_id).delete(
            synchronize_session=False
        )

        db.delete(event)
        db.commit()
    except Exception as e:
        db.rollback()
        logger_api.exception(f"Внутренняя ошибка сервера. Проблемы с сейвом БД: {e}")
        raise InternalServerError()

    return


async def del_ticket_type(
    db: Session,
    ticket_type_id: int,
    user_id: int,
) -> None:
    """
    Удаление типа мероприятия.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        ticket_type_id (int): ID типа билета.
        user_id (int): ID пользователя.

    Raises:
        ValidationError: Неверные данные.
        ForbiddenUserError: Отказано в доступе.
        InternalServerError: Ошибка сервера.
    """
    ticket_type = (
        db.query(TicketTypes)
        .join(Events)
        .filter(TicketTypes.id == ticket_type_id, Events.creator_id == user_id)
        .first()
    )

    if not ticket_type:
        exists = (
            db.query(TicketTypes.id).filter(TicketTypes.id == ticket_type_id).first()
        )
        if not exists:
            raise ValidationError()
        raise ForbiddenUserError()

    try:
        db.query(Tickets).filter(Tickets.ticket_type_id == ticket_type_id).delete(
            synchronize_session=False
        )

        db.delete(ticket_type)
        db.commit()
    except Exception as e:
        db.rollback()
        logger_api.exception(f"Внутренняя ошибка сервера. Проблемы с сейвом БД: {e}")
        raise InternalServerError()

    return


async def delete_data(
    db: Session,
    table_name: Literal["Accounts", "Events", "TicketTypes", "Tickets"],
    id: int,
    user_id: int | None,
) -> None:
    """
    Удаление элемента в таблице.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        table_name (Literal["Accounts", "Events", "TicketTypes", "Tickets"]): Название таблицы.
        id (int): Айди нужного элемента для удаления.

    Raises:
        ValidationError (HTTPException): Неверные данные.
    """

    data = db.get(config.GET_TABLE[table_name], id)
    if not data:
        raise ValidationError()

    if user_id is not None and user_id != data.user_id:
        raise ForbiddenUserError()

    db.delete(data)
    db.commit()
    return


async def db_activate_qr_code(
    db: Session, user_id: int, code: str
) -> "ActivateQrCodeResult":
    """
    Активация билета на мероприятие.

    Args:
        db (Session): Сессия SQLAlchemy для работы с БД.
        user_id (int): ID пользователя.
        code (str): Код билета.

    Raises:
        ValidationError (HTTPException): Неверные данные.
        ForbiddenError: Недостаточно прав для выполнения.
        InternalServerError: Ошибка сервера.

    Returns:
        ActivateQrCodeResult (TypedDict): Тело ответа.
    """
    ticket = db.query(Tickets).filter(Tickets.unique_code == code).first()

    if not ticket:
        raise ValidationError()

    if ticket.event.creator_id != user_id:
        raise ForbiddenError("Активировать билет может только создатель мероприятия")

    if ticket.is_used:
        return {"activate": False, "info": "Билет уже был активирован"}

    ticket.is_used = True
    db.commit()

    return {"activate": True, "info": "Билет успешно активирован"}


async def db_all_active_tickets_event(
    db: Session, event_id: int
) -> tuple[dict[str, int], int]:
    tickets = (
        db.query(Tickets)
        .options(joinedload(Tickets.ticket_type))
        .filter(Tickets.is_used == True, Tickets.event_id == event_id)
        .all()
    )

    result = defaultdict(int)
    total = 0
    for ticket in tickets:
        result[ticket.ticket_type.type] += 1
        total += 1
    return result, total


async def db_all_tickets_event(
    db: Session, event_id: int
) -> tuple[dict[str, int], int]:
    tickets = (
        db.query(Tickets)
        .options(joinedload(Tickets.ticket_type))
        .filter(Tickets.event_id == event_id)
        .all()
    )

    result = defaultdict(int)
    total = 0
    for ticket in tickets:
        result[ticket.ticket_type.type] += 1
        total += 1
    return result, total


async def db_get_info_user(db: Session, user_id: int):
    return db.query(Accounts).filter(Accounts.id == user_id).first()
