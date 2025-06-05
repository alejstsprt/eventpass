from typing import TYPE_CHECKING

from fastapi import APIRouter, Cookie, Depends, Path, status

from ...core.config import config
from ...infrastructure.cache import ICache, IClearCache
from ...schemas import ManagementTicketTypeProtocol, TicketCreateDTO
from ...services import get_tickets_service

router = APIRouter()


@router.post(
    "",
    summary="Создание билета на мероприятие",
    description="ИНФО: Ручка для создания билета на мероприятие. Принимает в ...",  # TODO: дописать
    status_code=status.HTTP_201_CREATED,
    responses=None,  # TODO: дописать
)
@IClearCache(unique_name="ticket-cache", jwt_token_path="jwt_token")
async def create_types_ticket(  # type: ignore[no-untyped-def]
    ticket_data: TicketCreateDTO,
    service: ManagementTicketTypeProtocol = Depends(get_tickets_service),
    jwt_token: str = Cookie(None),
):
    return await service.create_ticket(ticket_data, jwt_token)
