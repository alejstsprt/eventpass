from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Cookie, Path, Body
# from fastapi_cache.decorator import cache # имеет маленький функционал. я создал свой

from ...schemas import CreateEvent, EditEvent, ManagementEventsProtocol
from ...services import get_event_service, CREATE_EVENT_RESPONSES
from ...infrastructure.cache import IClearCache, ICache

router = APIRouter()


@router.post(
    '',
    summary="Создание мероприятия.",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя status, title, description, address.",
    responses=CREATE_EVENT_RESPONSES
)
@IClearCache(
    unique_name='event-cache',
    jwt_token_path='jwt_token'
)
async def create_event( # type: ignore[no-untyped-def]
        event: CreateEvent,
        service: ManagementEventsProtocol = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.create_events(jwt_token, event)


@router.patch(
    '/{event_id}',
    summary="Изменение мероприятия.",
    description="ИНФО: Ручка для изменения мероприятия. Принимает в себя status | None, title | None, description | None, address | None.",
    responses=None # TODO: дописать
)
@IClearCache(
    unique_name='event-cache',
    jwt_token_path='jwt_token'
)
async def edit_events( # type: ignore[no-untyped-def]
        event: EditEvent,
        event_id: int = Path(..., title="ID мероприятия", ge=1, le=9_223_372_036_854_775_807), # иначе будет ошибка бд
        jwt_token: str = Cookie(None),
        service: ManagementEventsProtocol = Depends(get_event_service),
    ):
    return await service.edit_events(jwt_token, event_id, event)


@router.get(
    '',
    summary="Список всех мероприятий.",
    description="ИНФО: Ручка для получения списка всех мероприятий.",
    responses=None # TODO: дописать
)
@ICache(
    unique_name='event-cache',
    jwt_token_path='jwt_token'
)
async def list_events( # type: ignore[no-untyped-def]
        service: ManagementEventsProtocol = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.all_events(jwt_token)