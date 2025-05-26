from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Cookie
# from fastapi_cache.decorator import cache

from ...schemas import CreateEvent
from ...services import get_event_service, CREATE_EVENT_RESPONSES
from ...core.logger import Logger

if TYPE_CHECKING:
    from ...services import ManagementEvents
    from ...schemas import EventCreatedResult
    from ...models.session import BaseModel


router = APIRouter()

logger = Logger("api_logger")

@router.post(
    '/add-events',
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя название, описание и адрес мероприятия.",
    responses=CREATE_EVENT_RESPONSES
)
async def add_events(
        event: CreateEvent,
        service: 'ManagementEvents' = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ) -> 'EventCreatedResult':
    return await service.create_events(jwt_token, event)

@router.post(
    '/all-events',
    summary="Список всех мероприятий",
    description="ИНФО: Ручка для получения списка всех мероприятий. Принимает в себя ...",
    responses=None
)
async def all_events(
        service: 'ManagementEvents' = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ) -> list['BaseModel']:
    return await service.all_events(jwt_token)