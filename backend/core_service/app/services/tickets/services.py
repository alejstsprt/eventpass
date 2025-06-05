from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

# from ...schemas import (
#     TicketCreateDTO
# )
from ...core.exceptions import NoTokenError, ValidationError
from ...models.crud import create_ticket_event
from ...schemas import TicketCreateResponseDTO
from ...security.hmac import generate_code_hmac_ticket
from ...security.jwt import token_verification

if TYPE_CHECKING:
    from ...models.models import TicketTypes
    from ...models.session import BaseModel as DBBaseModel
    from ...schemas import TicketCreateDTO


class ManagementTickets:
    """
    Модуль (класс) для управления билетами.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_ticket(self, data: "TicketCreateDTO", jwt_token: str):
        if not await token_verification(jwt_token):
            raise NoTokenError()

        unique_code = generate_code_hmac_ticket(
            data.event_id,
            data.user_id,
            data.ticket_type_id,
        )

        result = await create_ticket_event(
            self.db, data.event_id, data.user_id, data.ticket_type_id, unique_code
        )

        return TicketCreateResponseDTO.model_validate(result)
