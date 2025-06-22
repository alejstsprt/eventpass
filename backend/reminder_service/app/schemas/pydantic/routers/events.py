from typing import Annotated, Self

from app.core.config import config
from pydantic import BaseModel, Field, model_validator


# [AddEvent]
class EventsInfo(BaseModel):
    event_id: Annotated[
        int,
        Field(
            description="ID мероприятия",
            examples=[1],
            ge=1,
            le=config.MAX_ID,
        ),
    ]
    title: Annotated[
        str,
        Field(
            description="Название мероприятия",
            examples=["Желтый фургон"],
            min_length=1,
            max_length=1_000,
        ),
    ]
    address: Annotated[
        str,
        Field(
            description="Адрес мероприятия",
            examples=["СПБ, Ул. Пушкино, д.24"],
            min_length=1,
            max_length=1_000,
        ),
    ]


class AddEventsDTO(BaseModel):
    events: Annotated[
        list[EventsInfo],
        Field(description="Список мероприятий"),
    ]


# [EditEvent]
class EditEventDTO(BaseModel):
    title: Annotated[
        str | None,
        Field(
            description="Название мероприятия",
            examples=["Желтый фургон"],
            min_length=1,
            max_length=1_000,
        ),
    ] = None

    address: Annotated[
        str | None,
        Field(
            description="Адрес мероприятия",
            examples=["СПБ, Ул. Пушкино, д.24"],
            min_length=1,
            max_length=1_000,
        ),
    ] = None

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.title is None and self.address is None:
            raise ValueError("Укажите хотя бы один параметр")
        return self
