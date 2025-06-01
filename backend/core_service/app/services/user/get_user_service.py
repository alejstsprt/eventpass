from typing import TYPE_CHECKING

from fastapi import Depends

from ...models.session import get_db
from .user_services import ManagementUsers

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_user_service(db: "Session" = Depends(get_db)) -> ManagementUsers:
    """Функция возвращает созданную сессию БД"""
    return ManagementUsers(db)
