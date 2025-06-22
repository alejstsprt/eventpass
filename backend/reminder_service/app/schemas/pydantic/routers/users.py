from datetime import datetime
from typing import Annotated, Self

from app.core.config import config
from pydantic import BaseModel, EmailStr, Field, model_validator


# [AddUserInReminder]
class UsersInfo(BaseModel):
    name: Annotated[
        str,
        Field(
            description="Имя пользователя",
            examples=["user_name"],
            min_length=2,
            max_length=1_000,
        ),
    ]

    email: Annotated[
        EmailStr,
        Field(
            description="Почта пользователя",
            examples=["user_email@mail.ru"],
        ),
    ]

    event_id: Annotated[
        int | None,
        Field(
            description="ID мероприятия. Можно не указывать, если указано значение по умолчанию",
            examples=[1],
            ge=1,
            le=config.MAX_ID,
        ),
    ] = None

    text: Annotated[
        str | None,
        Field(
            description="Текст для уведомления. Можно не указывать, если указано значение по умолчанию. Можно указать {title} и {address} и все подставится автоматически",
            examples=[
                "Добрый день! Мероприятие {title} начнется уже завтра! Ждем вас!"
            ],
            min_length=10,
            max_length=5_000,
        ),
    ] = None

    start_event_at: Annotated[
        datetime | None,
        Field(
            description="Дата начала мероприятия. Уведомление придет за день до.",
        ),
    ] = None


class AddUserInReminderDTO(BaseModel):
    users: Annotated[
        list[UsersInfo],
        Field(
            description="Список пользователей",
        ),
    ]

    default_text: Annotated[
        str | None,
        Field(
            description="Значение по умолчанию. Подставится тем пользователям, у которых не указан текст",
            examples=[
                "Добрый день! Мероприятие {title} начнется уже завтра! Ждем вас!"
            ],
            min_length=10,
            max_length=5_000,
        ),
    ] = None

    default_event_id: Annotated[
        int | None,
        Field(
            description="Значение по умолчанию. Подставится тем пользователям, у которых не указан ID мероприятия",
            examples=[1],
            ge=1,
            le=config.MAX_ID,
        ),
    ] = None

    default_start_event_at: Annotated[
        datetime | None,
        Field(
            description="Значение по умолчанию. Подставится тем пользователям, у которых не указана дата начала мероприятия",
        ),
    ] = None


# [EditUser]
class EditUserDTO(BaseModel):
    name: Annotated[
        str | None,
        Field(
            description="Имя пользователя",
            examples=["user_name"],
            min_length=2,
            max_length=1_000,
        ),
    ] = None

    email: Annotated[
        EmailStr | None,
        Field(
            description="Почта пользователя",
            examples=["user_email@mail.ru"],
        ),
    ] = None

    text: Annotated[
        str | None,
        Field(
            description="Текст для уведомления. Можно не указывать, если указано значение по умолчанию. Можно указать {title} и {address} и все подставится автоматически",
            examples=[
                "Добрый день! Мероприятие {title} начнется уже завтра! Ждем вас!"
            ],
            min_length=10,
            max_length=5_000,
        ),
    ] = None

    start_at: Annotated[
        datetime | None,
        Field(
            description="Дата начала мероприятия. Уведомление придет за день до.",
        ),
    ] = None

    @model_validator(mode="after")
    def validate(self) -> Self:
        if (
            self.name is None
            and self.email is None
            and self.text is None
            and self.start_at is None
        ):
            raise ValueError("Укажите хотя бы один параметр")
        return self
