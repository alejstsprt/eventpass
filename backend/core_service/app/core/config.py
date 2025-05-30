import os

from typing import Literal
from dotenv import load_dotenv

from ..models.models import Accounts, Events, TicketTypes, Tickets


# Загружаем переменные из .env
load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY", 'atgeg4wetg4ge')
ALGORITHM: str = os.getenv("ALGORITHM", 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))

status_events: set = ('опубликовано', 'завершено', 'черновик') # FIXME: в user_tickets есть копия с использованием enum. потом сделаю масштабируемое + crud.py

# Для удобного взаимодействия алхимией
GET_TABLE: dict = {
    'Accounts': Accounts,
    'Events': Events,
    'TicketTypes': TicketTypes,
    'Tickets': Tickets,
} # копия в crud.py