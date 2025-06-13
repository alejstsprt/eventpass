from typing import TYPE_CHECKING

from models.crud import (
    create_type_ticket_event,
    del_ticket_type,
    edit_data,
    get_types_ticket_event,
)
from sqlalchemy.orm import Session

from core.exceptions import NoTokenError
from schemas import (
    CreateTicketTypeDTO,
    CreateTicketTypeResponseDTO,
    EditTicketTypeDTO,
    EditTicketTypeResponseDTO,
    GetTicketTypesResponseDTO,
)
from security.jwt import token_verification


class ManagementTicketTypes:
    """
    Модуль (класс) для управления мероприятиями.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_types_ticket_event(
        self, jwt_token: str, ticket_type_data: CreateTicketTypeDTO
    ) -> CreateTicketTypeResponseDTO:
        """
        Метод для создания типа билета для мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            ticket_type_data (CreateTicketTypeDTO): Данные для обновления.

        Returns:
            ...

        Raises:
            NoTokenError (Exception): Отсутствует/неправильный токен.
            ValidationError (HTTPException): Неверные данные.
            TicketTypeError (HTTPException): Данный тип билета для этого мероприяия уже существует.
            InternalServerError (HTTPException): Ошибка сервера.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        ticket_type = await create_type_ticket_event(
            self.db,
            ticket_type_data.event_id,
            ticket_type_data.ticket_type.value,
            ticket_type_data.description,
            ticket_type_data.price,
            ticket_type_data.total_count,
        )

        return CreateTicketTypeResponseDTO.model_validate(ticket_type)

    async def edit_types_ticket(
        self, jwt_token: str, types_ticket_id: int, ticket_type_data: EditTicketTypeDTO
    ) -> EditTicketTypeResponseDTO:
        """
        Обновляет тип билета для мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            types_ticket_id (int): ID редактируемого типа билета.
            ticket_type_data (EditTicketTypeDTO): Данные для обновления.

        Returns:
            DBBaseModel: Обновленный обьект типа билета.

        Raises:
            NoTokenError (HTTPException): Отсутствует/неправильный токен.
            ValidationError (HTTPException): Неверные данные.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        ticket_type = await edit_data(
            self.db, "TicketTypes", types_ticket_id, ticket_type_data
        )

        return EditTicketTypeResponseDTO.model_validate(ticket_type)

    async def search_types_ticket_event(
        self, jwt_token: str, event_id: int
    ) -> list[GetTicketTypesResponseDTO]:
        """
        Метод который возвращает все типы билета мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            event_id (int): ID мероприятия.

        Returns:
            DBBaseModel: Результат поиска.

        Raises:
            NoTokenError (HTTPException): Отсутствует/неправильный токен.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        ticket_types = await get_types_ticket_event(self.db, event_id)

        return [
            GetTicketTypesResponseDTO.model_validate(ticket_type)
            for ticket_type in ticket_types
        ]

    async def delete_ticket_type(self, jwt_token: str, ticket_type_id: int) -> None:
        """
        Удаление типа билета мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            ticket_type_id (int): ID типа билета.

        Raises:
            NoTokenError (HTTPException): Отсутствует/неправильный токен.
        """
        user_id = await token_verification(jwt_token)
        if not user_id:
            raise NoTokenError()

        await del_ticket_type(self.db, ticket_type_id, user_id)
        return
