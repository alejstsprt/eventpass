from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from ...schemas import CreateEvent
from ...models.crud import create_event, search_user, all_info_table
from ...security.jwt import token_verification
from ...core.exceptions import NoTokenError, TokenError

if TYPE_CHECKING:
    from ...schemas import EventCreatedResult
    from ...models.session import BaseModel


class ManagementEvents:
    """
    Модуль (класс) для управления мероприятиями.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_events(self, jwt_token: str, event: CreateEvent) -> 'EventCreatedResult':
        """
        Метод для создания мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            event (CreateEvent): Название, описание и адрес мероприятия.

        Returns:
            EventCreatedResult (TypedDict): Возвращает всю информацию о мероприятии, используя `create_event()`.

        Raises:
            NoTokenError (HTTPException): Токен отсутствует.
            TokenError (HTTPException): Неправильный токен.
            ValidationError (HTTPException): Неверные входные данные.
            InternalServerError (HTTPException): Ошибка сервера.
        """
        if not (user_id := await token_verification(jwt_token)):
            raise NoTokenError() # выбрасываем ошибку чтобы запутать, если попытка подделать токен. фронтенд поймет.

        is_user = await search_user(self.db, user_id=user_id)
        if is_user['id'] is None:
            raise TokenError()

        return await create_event(self.db, user_id, event.title, event.description, event.address)

    async def all_events(self, jwt_token: str) -> list:
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
            raise NoTokenError() # выбрасываем ошибку чтобы запутать, если попытка подделать токен. фронтенд поймет.

        return await all_info_table(self.db, 'Events')