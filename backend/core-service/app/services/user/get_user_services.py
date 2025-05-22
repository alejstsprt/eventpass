from fastapi import Depends
from sqlalchemy.orm import Session

from .user_services import CreateUser
from models.session import get_db


def get_create_user_services(db: Session = Depends(get_db)) -> CreateUser:
    return CreateUser(db)