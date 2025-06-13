from fastapi import APIRouter, Cookie, Depends, Path, status

from core.config import config
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
    summary="Количество купленных билетов мероприятия",
    description="ИНФО: Ручка для возврата количества купленных билетов.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
async def create_ticket(
    event_id: int = Path(..., title="ID мероприятия", ge=1, le=config.MAX_ID),
    service: ManagementTicketsProtocol = Depends(get_tickets_service),
    jwt_token: str = Cookie(None),
) -> AllTicketsEventResponseDTO:
    е
    return await service.all_tickets_event(jwt_token, event_id)


@router.get(
    "/{event_id}/active",
    summary="Количество активированных билетов мероприятия",
    description="ИНФО: Ручка для возврата количества активированных билетов.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
async def create_ticket(
    event_id: int = Path(..., title="ID мероприятия", ge=1, le=config.MAX_ID),
    service: ManagementTicketsProtocol = Depends(get_tickets_service),
    jwt_token: str = Cookie(None),
) -> AllActiveTicketsEventResponseDTO:
    return await service.all_active_tickets_event(jwt_token, event_id)


@router.post(
    "",
    summary="Создание билета на мероприятие",
    description="ИНФО: Ручка для создания билета на мероприятие. Принимает в себя event_id, ticket_type_id",
    status_code=status.HTTP_201_CREATED,
    responses=None,  # TODO: дописать
)
async def create_ticket(
    ticket_data: TicketCreateDTO,
    service: ManagementTicketsProtocol = Depends(get_tickets_service),
    jwt_token: str = Cookie(None),
) -> TicketCreateResponseDTO:
    return await service.create_ticket(ticket_data, jwt_token)


@router.post(
    "/scan/{code}",
    summary="Сканирование билета и его активация",
    description="ИНФО: Ручка для активации билета. Принимает уникальный код билета.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
async def create_ticket(
    code: str = Path(..., title="Уникальный код билета", min_length=2, max_length=1000),
    service: ManagementTicketsProtocol = Depends(get_tickets_service),
    jwt_token: str = Cookie(None),
) -> ActivateQrCodeResponseDTO:
    return await service.activate_qr_code(jwt_token, code)


@router.delete(
    "/{ticket_id}",
    summary="Удаление билета мероприятия",
    description="ИНФО: Удаляет билет по указанному ID. Принимает в себя айди билета.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_204_NO_CONTENT: {"description": "Успешное удаление"}},
)
async def delete_ticket(
    ticket_id: int = Path(..., title="ID билета", ge=1, le=config.MAX_ID),
    service: ManagementTicketsProtocol = Depends(get_tickets_service),
    jwt_token: str = Cookie(None),
) -> None:
    await service.delete_ticket(ticket_id, jwt_token)
    return
