from fastapi import Depends
from models.session import get_db
from sqlalchemy.orm import Session

from services.ticket_types.services import ManagementTicketTypes


def get_ticket_types_service(db: Session = Depends(get_db)) -> ManagementTicketTypes:
    """Функция возвращает созданную сессию БД"""
    return ManagementTicketTypes(db)
