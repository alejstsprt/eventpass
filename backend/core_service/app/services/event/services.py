from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from ...core.exceptions import NoTokenError, TokenError
from ...models.crud import all_info_table, create_event, edit_data, search_user
from ...schemas import (
    IntEventCreatorId,
    IntUserId,
    StrEventAddress,
    StrEventDescription,
    StrEventTitle,
)
from ...security.jwt import token_verification

if TYPE_CHECKING:
    from ...models.models import Events
    from ...models.session import BaseModel as DBBaseModel
    from ...schemas import CreateEvent, EditEvent


class ManagementEvents:
    """
    Модуль (класс) для управления мероприятиями.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_events(self, jwt_token: str, event: "CreateEvent") -> "Events":
        """
        Метод для создания мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            event (CreateEvent): Название, описание и адрес мероприятия.

        Returns:
            Events (DBBaseModel): Возвращает всю информацию о мероприятии, используя `create_event()`.

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

        return await create_event(
            self.db,
            IntEventCreatorId(user_id),
            event.status.value,
            StrEventTitle(event.title),
            event.category.value,
            StrEventDescription(event.description),
            StrEventAddress(event.address),
        )

    async def all_events(self, jwt_token: str) -> list["DBBaseModel"]:
        """
        Метод для вывода всех мероприятий (не оптимизирован для больших данных)

        Args:
            jwt_token (str): Токен пользователя.

        Returns:
            list[object]: Все мероприятия.

        Raises:
            NoTokenError (HTTPException): Токен отсутствует.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()  # выбрасываем ошибку чтобы запутать, если попытка подделать токен. фронтенд поймет.

        return await all_info_table(self.db, "Events")

    async def edit_events(
        self, jwt_token: str, event_id: int, event: "EditEvent"
    ) -> "DBBaseModel":
        """
        Редактирование данных мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            event_id (int): ID мероприятия.
            event (EditEvent): Данные которые нужно изменить.

        Returns:
            (list[Dict[str, Any]]): Вся информация об измененном обьекте.

        Raises:
            NoTokenError: Токен отстутствует/Неверный
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()  # выбрасываем ошибку чтобы запутать, если попытка подделать токен. фронтенд поймет.

        return await edit_data(self.db, "Events", event_id, event)
