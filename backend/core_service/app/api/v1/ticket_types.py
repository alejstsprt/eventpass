from typing import Annotated

from fastapi import APIRouter, Body, Cookie, Depends, Path, status
from fastapi_limiter.depends import RateLimiter

from core.config import config
from dependencies.injection_app import get_rabbit_producer
from infrastructure.cache.cache_v2 import ICache, ICacheWriter, IClearCache, IParam
from infrastructure.messaging.producer import RabbitProducer
from schemas import (
    CreateTicketTypeDTO,
    CreateTicketTypeResponseDTO,
    EditTicketTypeDTO,
    EditTicketTypeResponseDTO,
    GetTicketTypesResponseDTO,
    ManagementTicketTypeProtocol,
)
from security.jwt import token_verification
from services import get_ticket_types_service

router = APIRouter()


@router.get(
    "/{event_id}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Список типов билета мероприятия",
    description="ИНФО: Список типов билета мероприятия. Принимает только токен.",
    status_code=status.HTTP_200_OK,
)
@ICache(
    unique_name="ticket-types",
    tags=["ticket-types-1"],
    functions=[
        IParam(token_verification, "jwt_token"),
    ],
    data=["event_id"],
)
async def get_types_ticket_event(
    event_id: Annotated[
        int, Path(..., description="ID мероприятия", ge=1, le=config.MAX_ID)
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    service: Annotated[ManagementTicketTypeProtocol, Depends(get_ticket_types_service)],
) -> list[GetTicketTypesResponseDTO]:
    return await service.search_types_ticket_event(jwt_token, event_id)


@router.post(
    "",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Создание типа билета для мероприятия",
    description="ИНФО: Ручка для создания типа билета для мероприятия. Принимает в себя event_id, ticket_type, description, price, total_count.",
    status_code=status.HTTP_201_CREATED,
)
@IClearCache(
    unique_name="ticket-types",
    tags_delete=["ticket-types-1"],
)
async def create_types_ticket(
    ticket_type_data: Annotated[
        CreateTicketTypeDTO, Body(..., description="Данные о типе билета")
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    rabbit_producer: Annotated[RabbitProducer, Depends(get_rabbit_producer)],
    service: Annotated[ManagementTicketTypeProtocol, Depends(get_ticket_types_service)],
) -> CreateTicketTypeResponseDTO:
    return await service.create_types_ticket_event(
        jwt_token, ticket_type_data, rabbit_producer
    )


@router.patch(
    "/{ticket_type_id}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Изменение деталей типа билета мероприятия",
    description="ИНФО: Ручка для создания типа билета для мероприятия. Принимает в себя event_id | None, description | None, price | None, total_count | None.",
    status_code=status.HTTP_200_OK,
)
@IClearCache(
    unique_name="ticket-types",
    tags_delete=["ticket-types-1"],
)
async def edit_types_ticket(
    ticket_type_id: Annotated[
        int, Path(..., description="ID типа билета мероприятия", ge=1, le=config.MAX_ID)
    ],
    ticket_type_data: Annotated[
        EditTicketTypeDTO, Body(..., description="Новые данные типа билета")
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    service: Annotated[ManagementTicketTypeProtocol, Depends(get_ticket_types_service)],
) -> EditTicketTypeResponseDTO:
    return await service.edit_types_ticket(jwt_token, ticket_type_id, ticket_type_data)


@router.delete(
    "/{ticket_type_id}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Удаление типа билета мероприятия",
    description="ИНФО: Ручка для удаления типа билета мероприятия.",
    status_code=status.HTTP_204_NO_CONTENT,
)
@IClearCache(
    unique_name="ticket-types",
    tags_delete=["ticket-types-1"],
)
async def delete_types_ticket(
    ticket_type_id: Annotated[
        int, Path(..., description="ID типа билета мероприятия", ge=1, le=config.MAX_ID)
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    service: Annotated[ManagementTicketTypeProtocol, Depends(get_ticket_types_service)],
) -> None:
    await service.delete_ticket_type(jwt_token, ticket_type_id)
    return
