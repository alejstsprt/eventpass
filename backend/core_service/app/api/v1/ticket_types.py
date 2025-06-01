from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Cookie
# from fastapi_cache.decorator import cache # имеет маленький функционал. я создал свой

from ...schemas import CreateEvent, EditEvent, ManagementEventsProtocol
from ...services import get_event_service
from ...infrastructure.cache import IClearCache, ICache

router = APIRouter()


@router.post(
    '',
    summary="Создание типа мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя название, описание и адрес мероприятия.",
    responses=None # TODO: дописать
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