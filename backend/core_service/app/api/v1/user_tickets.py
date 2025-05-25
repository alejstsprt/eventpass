from typing import Optional

from fastapi import APIRouter, Depends, Cookie
from fastapi_cache.decorator import cache

from ...schemas.user_tickets import CreateEvent
from ...services.user_tickets.get_event_services import get_event_service
from ...services.user_tickets.user_tickets_services import ManagementEvents
from ...core.logger import Logger
from ...services.user_tickets.responses import CREATE_EVENT_RESPONSES


router = APIRouter()

logger = Logger("api_logger")

@router.post(
    '/add-events',
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя название, описание и адрес мероприятия.",
    responses=CREATE_EVENT_RESPONSES
)
async def create_user(
        event: CreateEvent,
        service: ManagementEvents = Depends(get_event_service),
        jwt_token: Optional[str] = Cookie(None)
    ):
    return await service.create_events(jwt_token, event)

@router.post(
    '/all-events',
    summary="Список всех мероприятий",
    description="ИНФО: Ручка для получения списка всех мероприятий. Принимает в себя ...",
    responses=None
)
async def create_user(
        service: ManagementEvents = Depends(get_event_service),
        jwt_token: Optional[str] = Cookie(None)
    ):
    return await service.all_events(jwt_token)