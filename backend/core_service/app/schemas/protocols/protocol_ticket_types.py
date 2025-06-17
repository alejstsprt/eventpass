from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from infrastructure.messaging.producer import RabbitProducer
    from models.models import TicketTypes
    from models.session import DBBaseModel
    from schemas import CreateTicketTypeDTO, EditTicketTypeDTO


class ManagementTicketTypeProtocol(Protocol):
    """Протокол ManagementTicketType"""

    async def create_types_ticket_event(
        self,
        jwt_token: str,
        ticket_type_data: "CreateTicketTypeDTO",
        rabbit_producer: "RabbitProducer",
    ) -> "TicketTypes":
        """
        Метод для создания типа билета для мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            ticket_type_data (CreateTicketTypeDTO): Пайдемик модель.

        Returns:
            TicketTypes

        Raises:
            NoTokenError (Exception): Токен отстуствует/неправильный.
            ValidationError (HTTPException): Неверные данные.
        """
        ...

    async def edit_types_ticket(
        self,
        jwt_token: str,
        types_ticket_id: int,
        ticket_type_data: "EditTicketTypeDTO",
    ) -> "DBBaseModel":
        """
        Обновляет тип билета для мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            types_ticket_id (int): ID редактируемого типа билета.
            ticket_type_data (EditTicketTypeDTO): Данные для обновления.

        Returns:
            BaseModel: Обновленный обьект типа билета.

        Raises:
            NoTokenError (HTTPException): Отсутствует/неправильный токен.
            ValidationError (HTTPException): Неверные данные.
        """
        ...

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
        ...

    async def delete_ticket_type(self, jwt_token: str, ticket_type_id: int) -> None:
        """
        Удаление типа билета мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            ticket_type_id (int): ID типа билета.

        Raises:
            NoTokenError (HTTPException): Отсутствует/неправильный токен.
        """
        ...
