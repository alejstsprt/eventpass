from fastapi import APIRouter, Cookie, Depends, Path, status
from fastapi_limiter.depends import RateLimiter

from core.config import config
from dependencies.injection_app import get_rabbit_producer
from infrastructure.cache.cache_v2 import ICache, IClearCache, IParam
from infrastructure.messaging.producer import RabbitProducer
from schemas import (
    AllElementsResponseDTO,
    CreateEventDTO,
    CreateEventResponseDTO,
    EditEventDTO,
    EditEventResponseDTO,
    ManagementEventsProtocol,
)
from security.jwt import token_verification
from services import CREATE_EVENT_RESPONSES, get_event_service

# from fastapi_cache.decorator import cache # имеет маленький функционал. я создал свой

router = APIRouter()


@router.get(
    "",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Список всех мероприятий",
    description="ИНФО: Ручка для получения списка всех мероприятий.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
@ICache(
    unique_name="event-cache",
    tags=["event-cache-1"],
    functions=[IParam(token_verification, "jwt_token")],
)
async def list_events(
    service: ManagementEventsProtocol = Depends(get_event_service),
    jwt_token: str = Cookie(None),  # TODO: сделать DI
) -> list[AllElementsResponseDTO]:
    return await service.all_events(jwt_token)


@router.post(
    "",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя status, title, description, address.",
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_EVENT_RESPONSES,
)
@IClearCache(
    unique_name="event-cache",
    tags_delete=["event-cache-1"],
)
async def create_event(
    event: CreateEventDTO,
    rabbit_producer: RabbitProducer = Depends(get_rabbit_producer),
    service: ManagementEventsProtocol = Depends(get_event_service),
    jwt_token: str = Cookie(None),
) -> CreateEventResponseDTO:
    return await service.create_events(jwt_token, event, rabbit_producer)


@router.patch(
    "/{event_id}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Изменение мероприятия",
    description="ИНФО: Ручка для изменения мероприятия. Принимает в себя status | None, title | None, description | None, address | None.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
@IClearCache(
    unique_name="event-cache",
    tags_delete=["event-cache-1"],
)
async def edit_events(
    event: EditEventDTO,
    event_id: int = Path(..., title="ID мероприятия", ge=1, le=config.MAX_ID),
    jwt_token: str = Cookie(None),
    service: ManagementEventsProtocol = Depends(get_event_service),
) -> EditEventResponseDTO:
    return await service.edit_events(jwt_token, event_id, event)


@router.delete(
    "/{event_id}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Удаление мероприятия",
    description="ИНФО: Ручка для удаления мероприятия по ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=None,  # TODO: дописать
)
@IClearCache(
    unique_name="event-cache",
    tags_delete=["event-cache-1"],
)
async def delete_events(
    event_id: int = Path(..., title="ID мероприятия", ge=1, le=config.MAX_ID),
    jwt_token: str = Cookie(None),
    service: ManagementEventsProtocol = Depends(get_event_service),
) -> None:
    await service.delete_event(jwt_token, event_id)
    return
