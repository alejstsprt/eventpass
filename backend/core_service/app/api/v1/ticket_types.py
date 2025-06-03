from typing import TYPE_CHECKING

from fastapi import APIRouter, Cookie, Depends

from ...infrastructure.cache import ICache, IClearCache
from ...schemas import CreateTicketType, ManagementTicketTypeProtocol
from ...services import get_ticket_types_service

router = APIRouter()


@router.post(
    "",
    summary="Создание типа билета для мероприятия",
    description="ИНФО: Ручка для создания типа билета для мероприятия. Принимает в себя event_id, ticket_type, description, price, total_count.",
    responses=None,  # TODO: дописать
)
@IClearCache(unique_name="ticket-types-cache", jwt_token_path="jwt_token")
async def create_event(  # type: ignore[no-untyped-def]
    ticket_type_data: CreateTicketType,
    service: ManagementTicketTypeProtocol = Depends(get_ticket_types_service),
    jwt_token: str = Cookie(None),
):
    return await service.create_types_ticket_event(jwt_token, ticket_type_data)
