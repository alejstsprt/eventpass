import os
from typing import Final, Type

from dotenv import load_dotenv

from ..models.models import Accounts, Events, Tickets, TicketTypes
from ..models.session import BaseModel

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
    # FIXME: в ticket_types есть копия с использованием enum. потом сделаю масштабируемое + crud.py
    TYPE_TICKETS: frozenset[str] = frozenset({"Vip", "Standard", "Econom"})

    # Для удобного взаимодействия c алхимией (копия в crud.py)
    GET_TABLE: dict[str, Type[BaseModel]] = {
        "Accounts": Accounts,
        "Events": Events,
        "TicketTypes": TicketTypes,
        "Tickets": Tickets,
    }

    # Лимит айди для БД
    MAX_ID: Final[int] = 9_223_372_036_854_775_807


config = Settings()
