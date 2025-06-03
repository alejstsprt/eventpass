from typing import TYPE_CHECKING

from fastapi import APIRouter, Cookie, Depends, Path, status

from ...core.config import config
from ...infrastructure.cache import ICache, IClearCache
from ...schemas import CreateTicketType, EditTicketType, ManagementTicketTypeProtocol
from ...services import get_ticket_types_service

router = APIRouter()


@router.post(
    "",
    summary="Создание типа билета для мероприятия",
    description="ИНФО: Ручка для создания типа билета для мероприятия. Принимает в себя event_id, ticket_type, description, price, total_count.",
    status_code=status.HTTP_201_CREATED,
    responses=None,  # TODO: дописать
)
@IClearCache(unique_name="ticket-types-cache", jwt_token_path="jwt_token")
async def create_types_ticket(  # type: ignore[no-untyped-def]
    ticket_type_data: CreateTicketType,
    service: ManagementTicketTypeProtocol = Depends(get_ticket_types_service),
    jwt_token: str = Cookie(None),
):
    return await service.create_types_ticket_event(jwt_token, ticket_type_data)


@router.patch(
    "/{types_ticket_id}",
    summary="Изменение деталей типа билета мероприятия",
    description="ИНФО: Ручка для создания типа билета для мероприятия. Принимает в себя event_id, ticket_type, description, price, total_count.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
@IClearCache(unique_name="ticket-types-cache", jwt_token_path="jwt_token")
async def edit_types_ticket(  # type: ignore[no-untyped-def]
    ticket_type_data: EditTicketType,
    types_ticket_id: int = Path(
        ..., title="ID типа билета мероприятия", ge=1, le=config.MAX_ID
    ),
    service: ManagementTicketTypeProtocol = Depends(get_ticket_types_service),
    jwt_token: str = Cookie(None),
):
    return await service.edit_types_ticket(jwt_token, types_ticket_id, ticket_type_data)
