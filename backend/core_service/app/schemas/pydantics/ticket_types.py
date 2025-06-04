from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


class TypeForm(str, Enum):
    """Типы мероприятия"""

    VIP = "Vip"
    STANDARD = "Standard"
    ECONOM = "Econom"


# [CreateTicketType]
class CreateTicketType(BaseModel):
    """Модель данных для создания типа мероприятия"""

    event_id: Annotated[int, Field(description="Айди мероприятия", examples=[1], ge=1)]

    ticket_type: Annotated[TypeForm, Field(description="Тип мероприятия")]

    description: Annotated[
        str,
        Field(
            description="Описание типа билета мероприятия",
            examples=["Это vip билет. Лучшие места."],
            min_length=10,
            max_length=10_000,
        ),
    ]

    price: Annotated[
        int,
        Field(
            description="Цена данного типа мероприятия",
            examples=[12_000],
            ge=1,
            le=1_000_000_000,
        ),
    ]

    total_count: Annotated[
        int,
        Field(
            description="Максимальное количество билетов на данный тип",
            examples=[100],
            ge=1,
            le=1_000_000_000,
        ),
    ]


# [EditTicketType]
class EditTicketType(BaseModel):
    """Модель данных для редактирования типа билета мероприятия"""

    description: Annotated[
        str | None,
        Field(
            description="Описание типа билета мероприятия",
            examples=["Это vip билет. Лучшие места."],
            min_length=10,
            max_length=10_000,
        ),
    ] = None

    price: Annotated[
        int | None,
        Field(
            description="Цена данного типа мероприятия",
            examples=[12_000],
            ge=1,
            le=1_000_000_000,
        ),
    ] = None

    total_count: Annotated[
        int | None,
        Field(
            description="Максимальное количество билетов на данный тип",
            examples=[100],
            ge=1,
            le=1_000_000_000,
        ),
    ] = None
