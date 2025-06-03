from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from pydantic import BaseModel

    from ...models.session import BaseModel as DBBaseModel
    from .. import CreateTicketType, EditTicketType


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

    async def edit_types_ticket(
        self, jwt_token: str, types_ticket_id: int, ticket_type_data: "EditTicketType"
    ) -> "BaseModel":
        """
        Обновляет тип билета для мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            types_ticket_id (int): ID редактируемого типа билета.
            ticket_type_data (EditTicketType): Данные для обновления.

        Returns:
            BaseModel: Обновленный обьект типа билета.

        Raises:
            NoTokenError (HTTPException): Отсутствует/неправильный токен.
            ValidationError (HTTPException): Неверные данные.
        """
        ...

    async def search_types_ticket_event(
        self, jwt_token: str, event_id: int
    ) -> "DBBaseModel":
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
        ...
