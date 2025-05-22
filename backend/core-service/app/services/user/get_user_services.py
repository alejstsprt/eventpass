from fastapi import Depends
from sqlalchemy.orm import Session

from .user_services import ManagementUsers
from ...models.session import get_db


def get_user_service(db: Session = Depends(get_db)) -> ManagementUsers:
    return ManagementUsers(db)