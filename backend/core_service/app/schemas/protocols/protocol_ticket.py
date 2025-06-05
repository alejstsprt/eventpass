from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .. import TicketCreateDTO, TicketCreateResponseDTO


class ManagementTicketsProtocol(Protocol):
    """Протокол ManagementTickets"""

    async def create_ticket(
        self, data: "TicketCreateDTO", jwt_token: str
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
