from typing import Annotated

from fastapi import APIRouter, Body, Cookie, Depends, File, Path, UploadFile, status
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
from services import get_event_service

# from fastapi_cache.decorator import cache # имеет маленький функционал. я создал свой

router = APIRouter()


@router.get(
    "",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Список всех мероприятий",
    description="ИНФО: Ручка для получения списка всех мероприятий.",
    status_code=status.HTTP_200_OK,
)
@ICache(
    unique_name="event-cache",
    tags=["event-cache-1"],
    functions=[IParam(token_verification, "jwt_token")],
)
async def list_events(
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],  # TODO: сделать DI
    service: Annotated[ManagementEventsProtocol, Depends(get_event_service)],
) -> list[AllElementsResponseDTO]:
    return await service.all_events(jwt_token)


@router.post(
    "",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя status, title, description, address.",
    status_code=status.HTTP_201_CREATED,
)
@IClearCache(
    unique_name="event-cache",
    tags_delete=["event-cache-1"],
)
async def create_event(
    file: Annotated[
        UploadFile,
        File(..., description="Изображение мероприятия", max_size=10_000_000),
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    event: Annotated[CreateEventDTO, Depends(CreateEventDTO.validate_form)],
    rabbit_producer: Annotated[RabbitProducer, Depends(get_rabbit_producer)],
    service: Annotated[ManagementEventsProtocol, Depends(get_event_service)],
) -> CreateEventResponseDTO:
    print(file)
    return await service.create_events(jwt_token, event, rabbit_producer)


@router.patch(
    "/{event_id}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Изменение мероприятия",
    description="ИНФО: Ручка для изменения мероприятия. Принимает в себя status | None, title | None, description | None, address | None.",
    status_code=status.HTTP_200_OK,
)
@IClearCache(
    unique_name="event-cache",
    tags_delete=["event-cache-1"],
)
async def edit_events(
    event_id: Annotated[
        int, Path(..., description="ID мероприятия", ge=1, le=config.MAX_ID)
    ],
    event: Annotated[EditEventDTO, Body(..., description="Новые данные мероприятия")],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    service: Annotated[ManagementEventsProtocol, Depends(get_event_service)],
) -> EditEventResponseDTO:
    return await service.edit_events(jwt_token, event_id, event)


@router.delete(
    "/{event_id}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Удаление мероприятия",
    description="ИНФО: Ручка для удаления мероприятия по ID.",
    status_code=status.HTTP_204_NO_CONTENT,
)
@IClearCache(
    unique_name="event-cache",
    tags_delete=["event-cache-1"],
)
async def delete_events(
    event_id: Annotated[
        int, Path(..., description="ID мероприятия", ge=1, le=config.MAX_ID)
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    service: Annotated[ManagementEventsProtocol, Depends(get_event_service)],
) -> None:
    await service.delete_event(jwt_token, event_id)
    return
