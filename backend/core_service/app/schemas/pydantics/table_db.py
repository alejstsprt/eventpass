"""
Какие данные таблиц могут вернуться пользователю.
"""

from datetime import datetime
from enum import Enum, unique

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


@unique
class TypeForm(str, Enum):
    """Типы мероприятия"""

    VIP = "Vip"
    STANDARD = "Standard"
    ECONOM = "Econom"


class AccountResponseDTO(ConfigBaseModelResponseDTO):
    """Таблица Accounts"""

    id: int
    name: str
    login: str


class EventResponseDTO(ConfigBaseModelResponseDTO):
    """Таблица Events"""

    id: int
    creator_id: int
    status: StatusForm
    category: CategoriesForm
    title: str
    description: str
    address: str
    datetime: datetime


class TicketTypeResponseDTO(ConfigBaseModelResponseDTO):
    """Таблица TicketTypes"""

    id: int
    event_id: int
    type: TypeForm
    description: str
    price: int
    total_count: int


class TicketResponseDTO(ConfigBaseModelResponseDTO):
    """Таблица Tickets"""

    id: int
    event_id: int
    user_id: int
    ticket_type_id: int
    unique_code: str
    is_used: bool
