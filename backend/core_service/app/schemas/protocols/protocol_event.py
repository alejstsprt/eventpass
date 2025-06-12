from typing import TYPE_CHECKING, Any, Dict, Protocol

if TYPE_CHECKING:
    from schemas import CreateEvent, EditEvent, EventCreatedResult


class ManagementEventsProtocol(Protocol):
    """Протокол ManagementEvents"""

    async def create_events(
        self, jwt_token: str, event: "CreateEvent"
    ) -> "EventCreatedResult":
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
        """ "
        Метод для вывода всех мероприятий (не оптимизирован для больших данных)

        Args:
            jwt_token (str): Токен пользователя.

        Returns:
            list[object]: Все мероприятия.

        Raises:
            NoTokenError (HTTPException): Токен отсутствует.
        """
        ...

    async def edit_events(
        self, jwt_token: str, event_id: int, event: "EditEvent"
    ) -> list[Dict[str, Any]]:
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
        ...

    async def delete_event(self, jwt_token: str, event_id: int) -> None:
        """
        Удаление мероприятия.

        Args:
            jwt_token (str): Токен пользователя.
            event_id (int): ID мероприятия.

        Raises:
            NoTokenError: Токен отстутствует/Неверный.
        """
        ...
