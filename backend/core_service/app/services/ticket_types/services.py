from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy.orm import Session

from ...core.exceptions import NoTokenError, TokenError
from ...models.crud import all_info_table, create_event, edit_info, search_user
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
    from ...schemas import CreateEvent, EditEvent, EventCreatedResult


class ManagementTicketTypes:
    """
    Модуль (класс) для управления мероприятиями.
    """

    def __init__(self, db: Session):
        self.db = db
