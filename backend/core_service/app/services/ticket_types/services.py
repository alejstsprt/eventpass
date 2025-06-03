from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy.orm import Session

from ...core.exceptions import NoTokenError, TokenError, ValidationError
from ...models.crud import create_type_ticket_event
from ...schemas import (
    IntEventCreatorId,
    IntUserId,
    StrEventAddress,
    StrEventDescription,
    StrEventTitle,
)
from ...security.jwt import token_verification

if TYPE_CHECKING:
    from ...models.session import BaseModel
    from ...schemas import CreateEvent, CreateTicketType, EditEvent, EventCreatedResult


class ManagementTicketTypes:
    """
    Модуль (класс) для управления мероприятиями.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_types_ticket_event(
        self, jwt_token: str, ticket_type_data: "CreateTicketType"
    ):
        """
        Метод для создания типа билета для мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            ticket_type_data (CreateTicketType): Пайдемик модель.

        Returns:
            CreateTicketType: None

        Raises:
            NoTokenError (Exception): Токен отстуствует/неправильный.
            ValidationError (HTTPException): Неверные данные.
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
            return ValidationError()

        return await create_type_ticket_event(
            self.db,
            ticket_type_data.event_id,
            ticket_type_data.ticket_type,
            ticket_type_data.description,
            ticket_type_data.price,
            ticket_type_data.total_count,
        )
