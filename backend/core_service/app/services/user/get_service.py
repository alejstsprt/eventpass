from fastapi import Depends
from models.session import get_db
from services.user.services import ManagementUsers
from sqlalchemy.orm import Session


def get_user_service(db: "Session" = Depends(get_db)) -> ManagementUsers:
    """Функция возвращает созданную сессию БД"""
    return ManagementUsers(db)
