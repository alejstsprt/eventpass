from typing import Protocol, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...schemas import EventCreatedResult, CreateEvent


class ManagementEventsProtocol(Protocol):
    async def create_events(self, jwt_token: str, event: 'CreateEvent') -> 'EventCreatedResult':
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
        ...

    async def all_events(self, jwt_token: str) -> list[Dict[str, Any]]:
        """"
        Метод для вывода всех мероприятий (не оптимизирован для больших данных)

        Args:
            jwt_token (str): Токен пользователя.

        Returns:
            list[object]: Все мероприятия.

        Raises:
            NoTokenError (HTTPException): Токен отсутствует.
        """
        ...

    async def edit_events(self, jwt_token: str, event) -> list: # TODO: доделать
        """Метод для редактирования мероприятия"""
        ...