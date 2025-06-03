from typing import TYPE_CHECKING, Any, Dict, Protocol

if TYPE_CHECKING:
    from .. import CreateEvent, CreateTicketType, EditEvent, EventCreatedResult


class ManagementTicketTypeProtocol(Protocol):
    """Протокол ManagementTicketType"""

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
        ...
