from fastapi import Depends
from sqlalchemy.orm import Session

from .user_services import CreateUser
from ...models.session import get_db


def get_user_service(db: Session = Depends(get_db)) -> CreateUser:
    return CreateUser(db)