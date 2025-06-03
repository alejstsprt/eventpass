from fastapi import Depends
from sqlalchemy.orm import Session

from ...models.session import get_db
from .services import ManagementTicketTypes


def get_ticket_types_service(db: Session = Depends(get_db)) -> ManagementTicketTypes:
    """Функция возвращает созданную сессию БД"""
    return ManagementTicketTypes(db)
