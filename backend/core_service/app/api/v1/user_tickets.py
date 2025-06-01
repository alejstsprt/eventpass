from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Cookie, Path, Body
# from fastapi_cache.decorator import cache # имеет маленький функционал. я создал свой

from ...schemas import CreateEvent, EditEvent, ManagementEventsProtocol
from ...services import get_event_service, CREATE_EVENT_RESPONSES
from ...infrastructure.cache import IClearCache, ICache

router = APIRouter()


@router.post(
    '/event',
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя название, описание и адрес мероприятия.",
    responses=CREATE_EVENT_RESPONSES
)
@IClearCache(
    unique_name='event-cache',
    jwt_token_path='jwt_token'
)
async def create_event(
        event: CreateEvent,
        service: ManagementEventsProtocol = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.create_events(jwt_token, event)


@router.patch(
    '/event/{event_id}',
    summary="Изменение мероприятия",
    description="ИНФО: Ручка для изменения мероприятия. Принимает в себя ...", # TODO: дописать
    responses=None # TODO: дописать
)
@IClearCache(
    unique_name='event-cache',
    jwt_token_path='jwt_token'
)
async def edit_events(
        event: EditEvent,
        event_id: int = Path(..., title="ID мероприятия", ge=1),
        jwt_token: str = Cookie(None),
        service: ManagementEventsProtocol = Depends(get_event_service),
    ):
    return await service.edit_events(jwt_token, event_id, event)


@router.get(
    '/event',
    summary="Список всех мероприятий",
    description="ИНФО: Ручка для получения списка всех мероприятий. Принимает в себя ...", # TODO: дописать
    responses=None # TODO: дописать
)
@ICache(
    unique_name='event-cache',
    jwt_token_path='jwt_token'
)
async def list_events(
        service: ManagementEventsProtocol = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.all_events(jwt_token)