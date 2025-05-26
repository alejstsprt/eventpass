from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Cookie
from fastapi_cache.decorator import cache

from ...schemas import CreateEvent, EditEvent
from ...services import get_event_service, CREATE_EVENT_RESPONSES

if TYPE_CHECKING:
    from ...services import ManagementEvents


router = APIRouter()

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
    ):
    return await service.create_events(jwt_token, event)

@router.patch(
    '/edit-events',
    summary="Изменение мероприятия",
    description="ИНФО: Ручка для изменения мероприятия. Принимает в себя ...",
    responses=None
)
async def edit_events(
        event: EditEvent,
        service: 'ManagementEvents' = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.edit_events(jwt_token, event)

@router.get(
    '/all-events',
    summary="Список всех мероприятий",
    description="ИНФО: Ручка для получения списка всех мероприятий. Принимает в себя ...",
    responses=None
)
# @cache(expire=80)
async def all_events(
        service: 'ManagementEvents' = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.all_events(jwt_token)