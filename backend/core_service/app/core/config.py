from dotenv import load_dotenv
from typing import Type
import os

from ..models.models import Accounts, Events, TicketTypes, Tickets
from ..models.session import BaseModel

# Загружаем переменные из .env
load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", 'atgeg4wetg4ge')
    ALGORITHM: str = os.getenv("ALGORITHM", 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10080))

    # FIXME: в user_tickets есть копия с использованием enum. потом сделаю масштабируемое + crud.py
    STATUS_EVENTS: frozenset[str] = frozenset({'опубликовано', 'завершено', 'черновик'})

    # Для удобного взаимодействия c алхимией
    GET_TABLE: dict[str, Type[BaseModel]] = {
        'Accounts': Accounts,
        'Events': Events,
        'TicketTypes': TicketTypes,
        'Tickets': Tickets,
    } # копия в crud.py

config = Settings()