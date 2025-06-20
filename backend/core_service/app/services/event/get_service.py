from fastapi import Depends
from sqlalchemy.orm import Session

from models.session import get_db
from services.event.services import ManagementEvents


def get_event_service(db: Session = Depends(get_db)) -> ManagementEvents:
    """Функция возвращает созданную сессию БД"""
    return ManagementEvents(db)
