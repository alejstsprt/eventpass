from sqlalchemy.orm import Session

from ...schemas.user_tickets import CreateEvent
from ...models.crud import create_event, search_user
from ...security.jwt import token_verification
from ...core.exceptions import NoTokenError, TokenError


class ManagementEvents:
    """
    Модуль (класс) для управления мероприятиями.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_events(self, jwt_token: str, event: CreateEvent) -> dict:
        """Метод для создания мероприятия"""
        if not (user_id := await token_verification(jwt_token)):
            raise NoTokenError() # выбрасываем ошибку чтобы запутать, если попытка подделать токен. фронтенд поймет.

        is_user = await search_user(self.db, user_id=user_id)
        if is_user['id'] is None:
            raise TokenError()

        return await create_event(self.db, user_id, event.title, event.description, event.address)