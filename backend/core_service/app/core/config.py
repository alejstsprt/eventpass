import os

from dotenv import load_dotenv

from ..models.models import Accounts, Events, TicketTypes, Tickets


# Загружаем переменные из .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", 'atgeg4wetg4ge')
ALGORITHM = os.getenv("ALGORITHM", 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))

GET_TABLE = {
    'Accounts': Accounts,
    'Events': Events,
    'TicketTypes': TicketTypes,
    'Tickets': Tickets,
}