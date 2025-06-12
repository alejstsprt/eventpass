from typing import TYPE_CHECKING

from models.crud import create_type_ticket_event, edit_data, get_types_ticket_event
from sqlalchemy.orm import Session

from core.exceptions import NoTokenError, ValidationError
from security.jwt import token_verification

if TYPE_CHECKING:
    from models.models import TicketTypes
    from models.session import DBBaseModel

    from schemas import CreateTicketType, EditTicketType


class ManagementTicketTypes:
    """
    Модуль (класс) для управления мероприятиями.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_types_ticket_event(
        self, jwt_token: str, ticket_type_data: "CreateTicketType"
    ) -> "TicketTypes":
        """
        Метод для создания типа билета для мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            ticket_type_data (CreateTicketType): Данные для обновления.

        Returns:
            CreateTicketType: None

        Raises:
            NoTokenError (Exception): Отсутствует/неправильный токен.
            ValidationError (HTTPException): Неверные данные.
            TicketTypeError (HTTPException): Данный тип билета для этого мероприяия уже существует.
            InternalServerError (HTTPException): Ошибка сервера.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        if (
            not ticket_type_data.event_id
            or not ticket_type_data.ticket_type
            or not ticket_type_data.description
            or not ticket_type_data.price
            or not ticket_type_data.total_count
        ):
            raise ValidationError()

        return await create_type_ticket_event(
            self.db,
            ticket_type_data.event_id,
            ticket_type_data.ticket_type.value,
            ticket_type_data.description,
            ticket_type_data.price,
            ticket_type_data.total_count,
        )

    async def edit_types_ticket(
        self, jwt_token: str, types_ticket_id: int, ticket_type_data: "EditTicketType"
    ) -> "DBBaseModel":
        """
        Обновляет тип билета для мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            types_ticket_id (int): ID редактируемого типа билета.
            ticket_type_data (EditTicketType): Данные для обновления.

        Returns:
            DBBaseModel: Обновленный обьект типа билета.

        Raises:
            NoTokenError (HTTPException): Отсутствует/неправильный токен.
            ValidationError (HTTPException): Неверные данные.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        return await edit_data(
            self.db, "TicketTypes", types_ticket_id, ticket_type_data
        )

    async def search_types_ticket_event(
        self, jwt_token: str, event_id: int
    ) -> list["TicketTypes"]:
        """
        Метод который возвращает все типы билета мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            event_id (int): ID мероприятия.

        Returns:
            DBBaseModel: Результат поиска.

        Raises:
            NoTokenError (HTTPException): Отсутствует/неправильный токен.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        return await get_types_ticket_event(self.db, event_id)
