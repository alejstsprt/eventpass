from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


class TypeForm(str, Enum):
    """Типы мероприятия"""

    VIP = "Vip"
    STANDARD = "Standard"
    ECONOM = "Econom"


class CreateTicketTypes(BaseModel):
    id: Annotated[int, Field(description="Айди мероприятия", examples=[1], ge=1)]

    type: Annotated[TypeForm, Field(description="Тип мероприятия")]

    description: Annotated[
        str,
        Field(
            description="Описание типа мероприятия",
            examples=["Это vip билет. Лучшие места."],
            min_length=10,
            max_length=10_000,
        ),
    ]

    price: Annotated[
        int,
        Field(
            description="Цена данного типа мероприятия",
            examples=[12000],
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
