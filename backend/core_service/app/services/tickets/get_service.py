from fastapi import Depends
from sqlalchemy.orm import Session

from ...models.session import get_db
from .services import ManagementTickets


def get_tickets_service(db: Session = Depends(get_db)) -> ManagementTickets:
    """Функция возвращает созданную сессию БД"""
    return ManagementTickets(db)
