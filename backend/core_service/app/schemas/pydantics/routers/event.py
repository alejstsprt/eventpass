from datetime import datetime
from enum import Enum, unique
from typing import Annotated, Self

from fastapi import Form
from pydantic import BaseModel, Field

from schemas.pydantics.cfg_base_model import ConfigBaseModelResponseDTO


@unique
class StatusForm(str, Enum):
    """Статусы мероприятия"""

    PUBLISHED = "опубликовано"
    COMPLETED = "завершено"
    DRAFT = "черновик"


@unique
class CategoriesForm(str, Enum):
    """Категории мероприятия"""

    CONCERT = "Концерт"
    FESTIVAL = "Фестиваль"
    CONFERENCE = "Конференция"
    EXHIBITION = "Выставка"
    SPORT = "Спорт"
    THEATRE = "Театр"
    OTHER = "Другое"


# [CreateEvent]
class CreateEventDTO(BaseModel):
    """Модель данных для создания мероприятия"""

    status: StatusForm
    title: str
    category: CategoriesForm
    description: str
    address: str

    @classmethod
    def validate_form(
        cls,
        status: Annotated[StatusForm, Form(..., description="Статус мероприятия")],
        title: Annotated[
            str,
            Form(
                ...,
                description="Название мероприятия",
                examples=["Конференция по Python"],
                min_length=2,
                max_length=50,
            ),
        ],
        category: Annotated[
            CategoriesForm, Form(..., description="Категория мероприятия")
        ],
        description: Annotated[
            str,
            Form(
                ...,
                description="Описание мероприятия",
                examples=["Ежегодная конференция для разработчиков"],
                min_length=10,
                max_length=10_000,
            ),
        ],
        address: Annotated[
            str,
            Form(
                ...,
                description="Адрес мероприятия",
                examples=["Ул. Штурманская, д. 30"],
                min_length=5,
                max_length=100,
            ),
        ],
    ) -> Self:
        return cls(**locals())


class CreateEventResponseDTO(ConfigBaseModelResponseDTO):
    id: int
    title: str
    category: str
    status: str
    description: str
    creator_id: int
    address: str
    datetime: datetime


# [EditEvent]
class EditEventDTO(BaseModel):
    """Модель данных для редактирования мероприятия"""

    status: Annotated[StatusForm | None, Field(description="Статус мероприятия")] = None

    title: Annotated[
        str | None,
        Field(
            description="Название мероприятия",
            examples=["Конференция по Python"],
            min_length=2,
            max_length=50,
        ),
    ] = None

    description: Annotated[
        str | None,
        Field(
            description="Описание мероприятия",
            examples=["Ежегодная конференция для разработчиков"],
            min_length=10,
            max_length=10_000,
        ),
    ] = None

    address: Annotated[
        str | None,
        Field(
            description="Адрес мероприятия",
            examples=["Ул. Штурманская, д. 30"],
            min_length=5,
            max_length=100,
        ),
    ] = None


class EditEventResponseDTO(CreateEventResponseDTO):
    pass


# [AllElements]
class AllElementsResponseDTO(CreateEventResponseDTO):
    pass
