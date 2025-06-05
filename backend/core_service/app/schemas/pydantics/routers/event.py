from enum import Enum
from typing import Annotated, NotRequired, Optional

from pydantic import BaseModel, Field


class StatusForm(str, Enum):
    """Статусы мероприятия"""

    PUBLISHED = "опубликовано"
    COMPLETED = "завершено"
    DRAFT = "черновик"


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
class CreateEvent(BaseModel):
    """Модель данных для создания мероприятия"""

    status: Annotated[StatusForm, Field(description="Статус мероприятия")]

    title: Annotated[
        str,
        Field(
            description="Название мероприятия",
            examples=["Конференция по Python"],
            min_length=2,
            max_length=50,
        ),
    ]

    category: Annotated[CategoriesForm, Field(description="Категория мероприятия")]

    description: Annotated[
        str,
        Field(
            description="Описание мероприятия",
            examples=["Ежегодная конференция для разработчиков"],
            min_length=10,
            max_length=10_000,
        ),
    ]

    address: Annotated[
        str,
        Field(
            description="Адрес мероприятия",
            examples=["Ул. Штурманская, д. 30"],
            min_length=5,
            max_length=100,
        ),
    ]


# [EditEvent]
class EditEvent(BaseModel):
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
