from typing import TYPE_CHECKING

from fastapi import APIRouter, Cookie, Depends, Path, status

from core.config import config
from infrastructure.cache_v2 import ICache, ICacheWriter, IClearCache, IParam
from schemas import CreateTicketType, EditTicketType, ManagementTicketTypeProtocol
from security.jwt import token_verification
from services import get_ticket_types_service

router = APIRouter()


@router.get(
    "/{event_id}",
    summary="Список типов билета мероприятия",
    description="ИНФО: Список типов билета мероприятия. Принимает только токен.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
@ICache(
    unique_name="ticket-types",
    tags=["ticket-types-1"],
    functions=[
        IParam(token_verification, "jwt_token"),
    ],
    data=["event_id"],
)
async def get_types_ticket_event(  # type: ignore[no-untyped-def]
    event_id: int = Path(..., title="ID мероприятия", ge=1, le=config.MAX_ID),
    service: ManagementTicketTypeProtocol = Depends(get_ticket_types_service),
    jwt_token: str = Cookie(None),
):
    return await service.search_types_ticket_event(jwt_token, event_id)


@router.post(
    "",
    summary="Создание типа билета для мероприятия",
    description="ИНФО: Ручка для создания типа билета для мероприятия. Принимает в себя event_id, ticket_type, description, price, total_count.",
    status_code=status.HTTP_201_CREATED,
    responses=None,  # TODO: дописать
)
@IClearCache(
    unique_name="ticket-types",
    tags_delete=["ticket-types-1"],
)
async def create_types_ticket(  # type: ignore[no-untyped-def]
    ticket_type_data: CreateTicketType,
    service: ManagementTicketTypeProtocol = Depends(get_ticket_types_service),
    jwt_token: str = Cookie(None),
):
    return await service.create_types_ticket_event(jwt_token, ticket_type_data)


@router.patch(
    "/{ticket_type_id}",
    summary="Изменение деталей типа билета мероприятия",
    description="ИНФО: Ручка для создания типа билета для мероприятия. Принимает в себя event_id | None, description | None, price | None, total_count | None.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: дописать
)
@IClearCache(
    unique_name="ticket-types",
    tags_delete=["ticket-types-1"],
)
async def edit_types_ticket(  # type: ignore[no-untyped-def]
    ticket_type_data: EditTicketType,
    ticket_type_id: int = Path(
        ..., title="ID типа билета мероприятия", ge=1, le=config.MAX_ID
    ),
    service: ManagementTicketTypeProtocol = Depends(get_ticket_types_service),
    jwt_token: str = Cookie(None),
):
    return await service.edit_types_ticket(jwt_token, ticket_type_id, ticket_type_data)


@router.delete(
    "/{ticket_type_id}",
    summary="Удаление типа билета мероприятия",
    description="ИНФО: Ручка для удаления типа билета мероприятия.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=None,  # TODO: дописать
)
@IClearCache(unique_name="ticket-types", tags_delete=["ticket-types-1"])
async def delete_types_ticket(
    ticket_type_id: int = Path(
        ..., title="ID типа билета мероприятия", ge=1, le=config.MAX_ID
    ),
    service: ManagementTicketTypeProtocol = Depends(get_ticket_types_service),
    jwt_token: str = Cookie(None),
) -> None:
    await service.delete_ticket_type(jwt_token, ticket_type_id)
    return
