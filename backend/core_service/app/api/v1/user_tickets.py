from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Cookie
# from fastapi_cache.decorator import cache # имеет маленький функционал. я создал свой

from ...schemas import CreateEvent, EditEvent, ManagementEventsProtocol
from ...services import get_event_service, CREATE_EVENT_RESPONSES
from ...infrastructure.cache import iClearCache, iCache

router = APIRouter()


@router.post(
    '/event',
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя название, описание и адрес мероприятия.",
    responses=CREATE_EVENT_RESPONSES
)
@iClearCache(unique_name='alexey')
async def create_event(
        event: CreateEvent,
        service: ManagementEventsProtocol = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.create_events(jwt_token, event)


@router.patch(
    '/event',
    summary="Изменение мероприятия",
    description="ИНФО: Ручка для изменения мероприятия. Принимает в себя ...", # TODO: дописать
    responses=None # TODO: дописать
)
async def edit_events(
        event: EditEvent,
        service: ManagementEventsProtocol = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.edit_events(jwt_token, event)


@router.get(
    '/event',
    summary="Список всех мероприятий",
    description="ИНФО: Ручка для получения списка всех мероприятий. Принимает в себя ...", # TODO: дописать
    responses=None # TODO: дописать
)
@iCache(
    unique_name='alexey',
    jwt_token_path='jwt_token',
    add_jwt_user_id=True
)
async def list_events(
        service: ManagementEventsProtocol = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.all_events(jwt_token)