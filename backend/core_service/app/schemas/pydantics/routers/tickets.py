from typing import Annotated

from pydantic import BaseModel, Field

from core.config import config
from schemas.pydantics.cfg_base_model import ConfigBaseModelResponseDTO
from schemas.pydantics.table_db import (
    AccountResponseDTO,
    EventResponseDTO,
    TicketTypeResponseDTO,
)


# [TicketCreate]
class TicketCreateDTO(BaseModel):
    """Модель для входных данных пользователя"""

    event_id: Annotated[
        int, Field(description="ID мероприятия", examples=[1], ge=1, le=config.MAX_ID)
    ]

    ticket_type_id: Annotated[
        int, Field(description="ID типа билета", examples=[1], ge=1, le=config.MAX_ID)
    ]


class TicketCreateResponseDTO(ConfigBaseModelResponseDTO):
    id: int
    event_id: int
    user_id: int
    ticket_type_id: int
    unique_code: str
    is_used: bool
    user: AccountResponseDTO
    ticket_type: TicketTypeResponseDTO
    event: EventResponseDTO


# [AllTicketsEvent]
class AllTicketsEventResponseDTO(ConfigBaseModelResponseDTO):
    total: int
    by_type: dict[str, int]


# [AllActiveTicketsEvent]
class AllActiveTicketsEventResponseDTO(AllTicketsEventResponseDTO):
    pass


# [ActivateQrCode]
class ActivateQrCodeResponseDTO(ConfigBaseModelResponseDTO):
    activate: str
    info: str
