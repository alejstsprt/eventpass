from fastapi import Depends
from models.session import get_db
from sqlalchemy.orm import Session

from services.user.services import ManagementUsers


def get_user_service(db: "Session" = Depends(get_db)) -> ManagementUsers:
    """Функция возвращает созданную сессию БД"""
    return ManagementUsers(db)
