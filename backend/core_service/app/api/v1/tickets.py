from core.config import config
from fastapi import APIRouter, Cookie, Depends, Path, status
from schemas import ManagementTicketsProtocol, TicketCreateDTO, TicketCreateResponseDTO
from services import get_tickets_service

router = APIRouter()


@router.post(
    "",
    summary="Создание билета на мероприятие",
    description="ИНФО: Ручка для создания билета на мероприятие. Принимает в себя event_id, ticket_type_id",
    status_code=status.HTTP_201_CREATED,
    responses=None,  # TODO: дописать
)
async def create_types_ticket(
    ticket_data: TicketCreateDTO,
    service: ManagementTicketsProtocol = Depends(get_tickets_service),
    jwt_token: str = Cookie(None),
) -> TicketCreateResponseDTO:
    return await service.create_ticket(ticket_data, jwt_token)


@router.delete(
    "/{ticket_id}",
    summary="Удаление билета мероприятия",
    description="ИНФО: Ручка для удаления билета мероприятия. Принимает в себя айди билета.",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=None,  # TODO: дописать
)
async def delete_types_ticket(
    ticket_id: int = Path(..., title="ID билета", ge=1, le=config.MAX_ID),
    service: ManagementTicketsProtocol = Depends(get_tickets_service),
    jwt_token: str = Cookie(None),
) -> None:
    return  # TODO: дописать
