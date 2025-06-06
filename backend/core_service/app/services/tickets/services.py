from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from ...core.exceptions import NoTokenError
from ...models.crud import create_ticket_event
from ...schemas import TicketCreateResponseDTO
from ...security.hmac import generate_code_hmac_ticket
from ...security.jwt import token_verification

if TYPE_CHECKING:
    from ...schemas import TicketCreateDTO


class ManagementTickets:
    """
    Модуль (класс) для управления билетами.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_ticket(
        self, data: "TicketCreateDTO", jwt_token: str
    ) -> TicketCreateResponseDTO:
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
        user_id = await token_verification(jwt_token)
        if not user_id:
            raise NoTokenError()

        unique_code = generate_code_hmac_ticket(
            data.event_id,
            user_id,
            data.ticket_type_id,
        )

        result = await create_ticket_event(
            self.db, data.event_id, user_id, data.ticket_type_id, unique_code
        )

        return TicketCreateResponseDTO.model_validate(result)
