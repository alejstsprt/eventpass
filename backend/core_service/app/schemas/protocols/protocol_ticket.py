from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from schemas import TicketCreateDTO, TicketCreateResponseDTO


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
