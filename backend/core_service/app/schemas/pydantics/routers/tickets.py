from typing import Annotated

from core.config import config
from pydantic import BaseModel, Field
from schemas.pydantics.cfg_base_model import ConfigBaseModelResponseDTO
from schemas.pydantics.table_db import (
    AccountResponseDTO,
    EventResponseDTO,
    TicketTypeResponseDTO,
)


class TicketCreateDTO(BaseModel):
    """Модель для входных данных пользователя"""

    event_id: Annotated[
        int, Field(description="ID мероприятия", examples=[1], ge=1, le=config.MAX_ID)
    ]

    ticket_type_id: Annotated[
        int, Field(description="ID типа билета", examples=[1], ge=1, le=config.MAX_ID)
    ]


class TicketCreateResponseDTO(ConfigBaseModelResponseDTO):
    """Модель для возврата данных при создании билета"""

    id: int
    event_id: int
    user_id: int
    ticket_type_id: int
    unique_code: str
    is_used: bool
    user: AccountResponseDTO
    ticket_type: TicketTypeResponseDTO
    event: EventResponseDTO
