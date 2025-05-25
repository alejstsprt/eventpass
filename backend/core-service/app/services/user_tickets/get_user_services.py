from fastapi import Depends
from sqlalchemy.orm import Session

from .user_tickets_services import ManagementEvents
from ...models.session import get_db


def get_event_service(db: Session = Depends(get_db)) -> ManagementEvents:
    return ManagementEvents(db)