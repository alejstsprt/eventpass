from fastapi import Depends
from models.session import get_db
from sqlalchemy.orm import Session

from services.tickets.services import ManagementTickets


def get_tickets_service(db: Session = Depends(get_db)) -> ManagementTickets:
    """Функция возвращает созданную сессию БД"""
    return ManagementTickets(db)
