from fastapi import Depends
from models.session import get_db
from services.tickets.services import ManagementTickets
from sqlalchemy.orm import Session


def get_tickets_service(db: Session = Depends(get_db)) -> ManagementTickets:
    """Функция возвращает созданную сессию БД"""
    return ManagementTickets(db)
