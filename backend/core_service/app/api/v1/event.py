from core.config import config
from fastapi import APIRouter, Cookie, Depends, Path, status
from infrastructure.cache import ICache, IClearCache
from schemas import CreateEvent, EditEvent, ManagementEventsProtocol
from services import CREATE_EVENT_RESPONSES, get_event_service

# from fastapi_cache.decorator import cache # имеет маленький функционал. я создал свой

router = APIRouter()


@router.post(
    "",
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя status, title, description, address.",
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_EVENT_RESPONSES,
)
@IClearCache(unique_name="event-cache", jwt_token_path="jwt_token")
async def create_event(  # type: ignore[no-untyped-def]
    event: CreateEvent,
    service: ManagementEventsProtocol = Depends(get_event_service),
    jwt_token: str = Cookie(None),
):
    return await service.create_events(jwt_token, event)


@router.patch(
    "/{event_id}",
    summary="Изменение мероприятия",
    description="ИНФО: Ручка для изменения мероприятия. Принимает в себя status | None, title | None, description | None, address | None.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
@IClearCache(unique_name="event-cache", jwt_token_path="jwt_token")
async def edit_events(  # type: ignore[no-untyped-def]
    event: EditEvent,
    event_id: int = Path(
        ..., title="ID мероприятия", ge=1, le=config.MAX_ID
    ),  # иначе будет ошибка бд
    jwt_token: str = Cookie(None),
    service: ManagementEventsProtocol = Depends(get_event_service),
):
    return await service.edit_events(jwt_token, event_id, event)


@router.get(
    "",
    summary="Список всех мероприятий",
    description="ИНФО: Ручка для получения списка всех мероприятий.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
@ICache(unique_name="event-cache", jwt_token_path="jwt_token")
async def list_events(  # type: ignore[no-untyped-def]
    service: ManagementEventsProtocol = Depends(get_event_service),
    jwt_token: str = Cookie(None),
):
    return await service.all_events(jwt_token)


@router.delete(
    "/{event_id}",
    summary="Удаление мероприятия",
    description="ИНФО: Ручка для удаления мероприятия по ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=None,  # TODO: дописать
)
@IClearCache(unique_name="event-cache", jwt_token_path="jwt_token")
async def delete_events(
    event_id: int = Path(
        ..., title="ID мероприятия", ge=1, le=config.MAX_ID
    ),  # иначе будет ошибка бд
    jwt_token: str = Cookie(None),
    service: ManagementEventsProtocol = Depends(get_event_service),
) -> None:
    return  # TODO: реализовать
