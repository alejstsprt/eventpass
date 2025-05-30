from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Cookie
# from fastapi_cache.decorator import cache # имеет маленький функционал. я создал свой

from ...schemas import CreateEvent, EditEvent
from ...services import get_event_service, CREATE_EVENT_RESPONSES
from ...infrastructure.cache import IClearCache, ICache

if TYPE_CHECKING:
    from ...services import ManagementEvents

router = APIRouter()


@router.post(
    '/add-events',
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя название, описание и адрес мероприятия.",
    responses=CREATE_EVENT_RESPONSES
)
@IClearCache(unique_name='alexey')
async def add_events(
        event: CreateEvent,
        service: 'ManagementEvents' = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.create_events(jwt_token, event)


@router.patch(
    '/edit-events',
    summary="Изменение мероприятия",
    description="ИНФО: Ручка для изменения мероприятия. Принимает в себя ...", # TODO: дописать
    responses=None
)
@ICache(
    unique_name='alexey',
    jwt_token_path='jwt_token',
    add_pydantic_model='event',
    add_jwt_token=True,
    add_jwt_user_id=True
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
    description="ИНФО: Ручка для получения списка всех мероприятий. Принимает в себя ...", # TODO: дописать
    responses=None
)
@ICache(
    unique_name='alexey',
    jwt_token_path='jwt_token',
    add_jwt_user_id=True
)
async def all_events(
        service: 'ManagementEvents' = Depends(get_event_service),
        jwt_token: str = Cookie(None)
    ):
    return await service.all_events(jwt_token)