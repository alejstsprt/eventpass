from typing import Union

from sqlalchemy.orm import Session
from fastapi import Response

from ...schemas.user_tickets import *
from ...models.crud import user_registration
from ...models.models import Accounts, Events, TicketTypes, Tickets
from ...security.hashing import hash_password, verify_password
from ...security.jwt import set_jwt_cookie, create_access_token
from ...core.exceptions import (
        LoginAlreadyExistsException,
        ValidationError,
        PasswordError,
        LoginError,
        InternalServerError
    )


class ManagementEvents:
    """Модуль для управления пользователем пользователем.

    `create_user(user: LoginUser)` - создать пользователя
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_events(self, response: Response, user: CreateUser) -> dict:
        pass