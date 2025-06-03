from typing import TYPE_CHECKING

from fastapi import APIRouter, Cookie, Depends

from ...infrastructure.cache import ICache, IClearCache
from ...schemas import CreateTicketTypes, ManagementTicketTypesProtocol
from ...services import get_ticket_types_service

router = APIRouter()


@router.post(
    "",
    summary="Создание типа мероприятия",
    description="ИНФО: Ручка для создания типа мероприятия. Принимает в себя ...",  # TODO: дописать
    responses=None,  # TODO: дописать
)
@IClearCache(unique_name="ticket-types-cache", jwt_token_path="jwt_token")
async def create_event(  # type: ignore[no-untyped-def]
    event: CreateTicketTypes,
    service: ManagementTicketTypesProtocol = Depends(get_ticket_types_service),
    jwt_token: str = Cookie(None),
):
    return await service.create_events(jwt_token, event)
