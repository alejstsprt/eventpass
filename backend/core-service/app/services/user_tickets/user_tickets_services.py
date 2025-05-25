from typing import Union

from sqlalchemy.orm import Session
from fastapi import Response

from ...schemas.user_tickets import CreateEvent
from ...models.crud import create_event
from ...models.models import Accounts, Events, TicketTypes, Tickets
from ...security.jwt import token_verification
from ...core.exceptions import (
        NoTokenError
    )


class ManagementEvents:
    """
    Модуль для управления мероприятиями.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_events(self, jwt_token: str, event: CreateEvent) -> dict:
        if not (user_id := await token_verification(jwt_token)):
            raise NoTokenError()

        return await create_event(self.db, user_id, event.title, event.description, event.address)