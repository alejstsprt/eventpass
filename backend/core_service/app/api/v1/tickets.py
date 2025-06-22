from typing import Annotated

from fastapi import APIRouter, Body, Cookie, Depends, Path, status
from fastapi_limiter.depends import RateLimiter

from core.config import config
from dependencies.injection_app import get_rabbit_producer
from infrastructure.messaging.producer import RabbitProducer
from schemas import (
    ActivateQrCodeResponseDTO,
    AllActiveTicketsEventResponseDTO,
    AllTicketsEventResponseDTO,
    ManagementTicketsProtocol,
    TicketCreateDTO,
    TicketCreateResponseDTO,
)
from services import get_tickets_service

router = APIRouter()


@router.get(
    "/{event_id}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Количество купленных билетов мероприятия",
    description="ИНФО: Ручка для возврата количества купленных билетов.",
    status_code=status.HTTP_200_OK,
)
async def get_ticket_all(
    event_id: Annotated[
        int, Path(..., description="ID мероприятия", ge=1, le=config.MAX_ID)
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    service: Annotated[ManagementTicketsProtocol, Depends(get_tickets_service)],
) -> AllTicketsEventResponseDTO:
    return await service.all_tickets_event(jwt_token, event_id)


@router.get(
    "/{event_id}/active",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Количество активированных билетов мероприятия",
    description="ИНФО: Ручка для возврата количества активированных билетов.",
    status_code=status.HTTP_200_OK,
)
async def get_ticket_active(
    event_id: Annotated[
        int, Path(..., description="ID мероприятия", ge=1, le=config.MAX_ID)
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    service: Annotated[ManagementTicketsProtocol, Depends(get_tickets_service)],
) -> AllActiveTicketsEventResponseDTO:
    return await service.all_active_tickets_event(jwt_token, event_id)


@router.post(
    "",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Создание билета на мероприятие",
    description="ИНФО: Ручка для создания билета на мероприятие. Принимает в себя event_id, ticket_type_id",
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(
    ticket_data: Annotated[
        TicketCreateDTO, Body(..., description="Данные для создания билета")
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    rabbit_producer: Annotated[RabbitProducer, Depends(get_rabbit_producer)],
    service: Annotated[ManagementTicketsProtocol, Depends(get_tickets_service)],
) -> TicketCreateResponseDTO:
    return await service.create_ticket(ticket_data, jwt_token, rabbit_producer)


@router.post(
    "/scan/{code}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Сканирование билета и его активация",
    description="ИНФО: Ручка для активации билета. Принимает уникальный код билета.",
    status_code=status.HTTP_200_OK,
)
async def scan_ticket(
    code: Annotated[
        str,
        Path(..., description="Уникальный код билета", min_length=2, max_length=1000),
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    rabbit_producer: Annotated[RabbitProducer, Depends(get_rabbit_producer)],
    service: Annotated[ManagementTicketsProtocol, Depends(get_tickets_service)],
) -> ActivateQrCodeResponseDTO:
    return await service.activate_qr_code(jwt_token, code, rabbit_producer)


@router.delete(
    "/{ticket_id}",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Удаление билета мероприятия",
    description="ИНФО: Удаляет билет по указанному ID. Принимает в себя айди билета.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_ticket(
    ticket_id: Annotated[
        int, Path(..., description="ID билета", ge=1, le=config.MAX_ID)
    ],
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    service: Annotated[ManagementTicketsProtocol, Depends(get_tickets_service)],
) -> None:
    await service.delete_ticket(ticket_id, jwt_token)
    return
