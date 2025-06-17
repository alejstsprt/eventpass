import os
from typing import Final, Type

from dotenv import load_dotenv
from models.models import Accounts, Events, Tickets, TicketTypes
from models.session import DBBaseModel

# Загружаем переменные из .env
load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "atgeg4wetg4ge")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10080)
    )

    # FIXME: в event есть копия с использованием enum. потом сделаю масштабируемое + crud.py
    STATUS_EVENTS: frozenset[str] = frozenset({"опубликовано", "завершено", "черновик"})
    # FIXME: в event есть копия с использованием enum. потом сделаю масштабируемое + crud.py
    CATEGORY_EVENTS: frozenset[str] = frozenset(
        {"Концерт", "Фестиваль", "Конференция", "Выставка", "Спорт", "Театр", "Другое"}
    )
    # FIXME: в ticket_types есть копия с использованием enum. потом сделаю масштабируемое + crud.py
    TYPE_TICKETS: frozenset[str] = frozenset({"Vip", "Standard", "Econom"})

    # Для удобного взаимодействия c алхимией (копия в crud.py)
    GET_TABLE: dict[str, Type[DBBaseModel]] = {
        "Accounts": Accounts,
        "Events": Events,
        "TicketTypes": TicketTypes,
        "Tickets": Tickets,
    }

    # Лимит айди для БД
    MAX_ID: Final[int] = 9_223_372_036_854_775_807

    # для генерации уникального кода билета
    SECRET_KEY_HMAC: bytes = os.getenv(
        "SECRET_KEY_HMAC", "ewgewgwgew22222222fee"
    ).encode()

    # для раббита
    RABBIT_USER: str = os.getenv("RABBIT_USER", "eventpass")
    RABBIT_PASSWORD: str = os.getenv("RABBIT_PASSWORD", "eventpass12345")


config = Settings()
