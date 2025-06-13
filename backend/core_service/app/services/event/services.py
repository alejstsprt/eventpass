from typing import TYPE_CHECKING

from models.crud import all_info_table, create_event, del_event, edit_data, search_user
from sqlalchemy.orm import Session

from core.exceptions import NoTokenError, TokenError
from schemas import (
    AllElementsResponseDTO,
    CreateEventResponseDTO,
    EditEventResponseDTO,
    IntEventCreatorId,
    IntUserId,
    StrEventAddress,
    StrEventDescription,
    StrEventTitle,
)
from security.jwt import token_verification

if TYPE_CHECKING:
    from schemas import CreateEventDTO, EditEventDTO


class ManagementEvents:
    """
    Модуль (класс) для управления мероприятиями.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_events(
        self, jwt_token: str, event: "CreateEventDTO"
    ) -> CreateEventResponseDTO:
        """
        Метод для создания мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            event (CreateEventDTO): Название, описание и адрес мероприятия.

        Returns:
            CreateEventResponseDTO (BaseModel): Возвращает всю информацию о мероприятии, используя `create_event()`.

        Raises:
            NoTokenError (HTTPException): Токен отсутствует.
            TokenError (HTTPException): Неправильный токен.
            ValidationError (HTTPException): Неверные входные данные.
            InternalServerError (HTTPException): Ошибка сервера.
        """
        if not (user_id := await token_verification(jwt_token)):
            raise NoTokenError()  # выбрасываем ошибку чтобы запутать, если попытка подделать токен. фронтенд поймет.

        is_user = await search_user(self.db, user_id=IntUserId(user_id))
        if is_user["id"] is None:
            raise TokenError()

        event = await create_event(
            self.db,
            IntEventCreatorId(user_id),
            event.status.value,
            StrEventTitle(event.title),
            event.category.value,
            StrEventDescription(event.description),
            StrEventAddress(event.address),
        )

        return CreateEventResponseDTO.model_validate(event)

    async def all_events(self, jwt_token: str) -> list[AllElementsResponseDTO]:
        """
        Метод для вывода всех мероприятий (не оптимизирован для больших данных).

        Args:
            jwt_token (str): Токен пользователя.

        Returns:
           AllElementsResponseDTO (list[BaseModel]): Все мероприятия.

        Raises:
            NoTokenError (HTTPException): Токен отсутствует.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        events = await all_info_table(self.db, "Events")

        return [AllElementsResponseDTO.model_validate(event) for event in events]

    async def edit_events(
        self, jwt_token: str, event_id: int, event: "EditEventDTO"
    ) -> EditEventResponseDTO:
        """
        Редактирование данных мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            event_id (int): ID мероприятия.
            event (EditEventDTO): Данные которые нужно изменить.

        Returns:
            EditEventResponseDTO (BaseModel): Вся информация об измененном обьекте.

        Raises:
            NoTokenError: Токен отстутствует/Неверный.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        event = await edit_data(self.db, "Events", event_id, event)

        return EditEventResponseDTO.model_validate(event)

    async def delete_event(self, jwt_token: str, event_id: int) -> None:
        """
        Удаление мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            event_id (int): ID мероприятия.

        Raises:
            NoTokenError: Токен отстутствует/Неверный.
        """
        user_id = await token_verification(jwt_token)
        if not user_id:
            raise NoTokenError()

        await del_event(self.db, event_id, user_id)

        return
