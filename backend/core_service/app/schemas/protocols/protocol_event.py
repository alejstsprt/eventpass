from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from infrastructure.messaging.producer import RabbitProducer
    from schemas import (
        AllElementsResponseDTO,
        CreateEventDTO,
        CreateEventResponseDTO,
        EditEventDTO,
        EditEventResponseDTO,
    )


class ManagementEventsProtocol(Protocol):
    """Протокол ManagementEvents"""

    async def create_events(
        self,
        jwt_token: str,
        event: "CreateEventDTO",
        rabbit_producer: "RabbitProducer",
    ) -> "CreateEventResponseDTO":
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
        ...

    async def all_events(self, jwt_token: str) -> list["AllElementsResponseDTO"]:
        """
        Метод для вывода всех мероприятий (не оптимизирован для больших данных).

        Args:
            jwt_token (str): Токен пользователя.

        Returns:
           AllElementsResponseDTO (list[BaseModel]): Все мероприятия.

        Raises:
            NoTokenError (HTTPException): Токен отсутствует.
        """
        ...

    async def edit_events(
        self, jwt_token: str, event_id: int, event: "EditEventDTO"
    ) -> "EditEventResponseDTO":
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
