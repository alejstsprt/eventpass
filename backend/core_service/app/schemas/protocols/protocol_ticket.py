from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from infrastructure.messaging.producer import RabbitProducer
    from schemas import (
        ActivateQrCodeResponseDTO,
        AllActiveTicketsEventResponseDTO,
        AllTicketsEventResponseDTO,
        TicketCreateDTO,
        TicketCreateResponseDTO,
    )


class ManagementTicketsProtocol(Protocol):
    """Протокол ManagementTickets"""

    async def create_ticket(
        self,
        data: "TicketCreateDTO",
        jwt_token: str,
        rabbit_producer: "RabbitProducer",
    ) -> "TicketCreateResponseDTO":
        """
        Метод для создания билета на мероприятие.

        Args:
            data (TicketCreateDTO): Данные для создания билета.
            jwt_token (str): JWT токен пользователя.

        Returns:
            TicketCreateResponseDTO: Возвращает данные о созданном билете.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        ...

    async def delete_ticket(self, ticket_id: int, jwt_token: str) -> None:
        """
        Метод для удаления билета.

        Args:
            ticket_id (int): ID билета.
            jwt_token (str): JWT токен пользователя.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        ...

    async def activate_qr_code(
        self, jwt_token: str, code: str, rabbit_producer: "RabbitProducer"
    ) -> "ActivateQrCodeResponseDTO":
        """
        Метод для активации кьюаркода.

        Args:
            jwt_token (str): JWT токен пользователя.
            code (str): Уникальный код билета

        Returns:
            ActivateQrCodeResponseDTO (BaseModel): Возвращает пайдемик модель.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        ...

    async def all_active_tickets_event(
        self, jwt_token: str, event_id: int
    ) -> "AllActiveTicketsEventResponseDTO":
        """
        Метод для получения активированных билетов мероприятия.

        Args:
            jwt_token (str): JWT токен пользователя.
            event_id (int): ID мероприятия.

        Returns:
            AllActiveTicketsEventResponseDTO (BaseModel): Возвращает пайдемик модель.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        ...

    async def all_tickets_event(
        self, jwt_token: str, event_id: int
    ) -> "AllTicketsEventResponseDTO":
        """
        Метод для получения всех билетов мероприятия.

        Args:
            jwt_token (str): JWT токен пользователя.
            event_id (int): ID мероприятия.

        Returns:
            AllTicketsEventResponseDTO (BaseModel): Возвращает пайдемик модель.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        ...
