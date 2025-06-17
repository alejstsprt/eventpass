from sqlalchemy.orm import Session

from core.config import config
from core.exceptions import NoTokenError
from infrastructure.messaging.producer import RabbitProducer
from models.crud import (
    create_ticket_event,
    db_activate_qr_code,
    db_all_active_tickets_event,
    db_all_tickets_event,
    delete_data,
    search_user,
)
from schemas import (
    ActivateQrCodeResponseDTO,
    AllActiveTicketsEventResponseDTO,
    AllTicketsEventResponseDTO,
    IntUserId,
    TicketCreateDTO,
    TicketCreateResponseDTO,
)
from security.hmac import generate_code_hmac_ticket
from security.jwt import token_verification


class ManagementTickets:
    """
    Модуль (класс) для управления билетами.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_ticket(
        self,
        data: "TicketCreateDTO",
        jwt_token: str,
        rabbit_producer: RabbitProducer,
    ) -> TicketCreateResponseDTO:
        """
        Метод для создания билета на мероприятие.

        Args:
            data (TicketCreateDTO): Данные для создания билета.
            jwt_token (str): JWT токен пользователя.

        Returns:
            TicketCreateResponseDTO: Возвращает данные о созданном билете.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        user_id = await token_verification(jwt_token)
        if not user_id:
            raise NoTokenError()

        unique_code = generate_code_hmac_ticket(
            data.event_id,
            user_id,
            data.ticket_type_id,
        )

        result = await create_ticket_event(
            self.db, data.event_id, user_id, data.ticket_type_id, unique_code
        )

        await rabbit_producer.add_to_queue(
            config.QUEUE_NAME,
            {
                "type": "email",
                "payload": {
                    "to": f"{result.user.login}",
                    "title": "Покупка билета",
                    "text": f"{result.user.name}, спасибо за покупку билета на мероприятие '{result.event.title}'. Вы купили '{result.ticket_type.type}' билет за {result.ticket_type.price} рублей",
                },
            },
        )

        return TicketCreateResponseDTO.model_validate(result)

    async def delete_ticket(self, ticket_id: int, jwt_token: str) -> None:
        """
        Метод для удаления билета.

        Args:
            ticket_id (int): ID билета.
            jwt_token (str): JWT токен пользователя.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        user_id = await token_verification(jwt_token)
        if not user_id:
            raise NoTokenError()

        await delete_data(self.db, "Tickets", ticket_id, user_id)
        return

    async def activate_qr_code(
        self, jwt_token: str, code: str, rabbit_producer: RabbitProducer
    ) -> ActivateQrCodeResponseDTO:
        """
        Метод для активации кьюаркода.

        Args:
            jwt_token (str): JWT токен пользователя.
            code (str): Уникальный код билета

        Returns:
            ActivateQrCodeResponseDTO (BaseModel): Возвращает пайдемик модель.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        user_id = await token_verification(jwt_token)
        if not user_id:
            raise NoTokenError()

        user = await search_user(self.db, user_id=IntUserId(user_id))

        result = await db_activate_qr_code(self.db, user_id, code)

        if result["activate"]:
            await rabbit_producer.add_to_queue(
                config.QUEUE_NAME,
                {
                    "type": "email",
                    "payload": {
                        "to": f"{user['id'].login}",
                        "title": "Активация билета",
                        "text": f"{user['id'].name}, ваш билет был успешно активирован. Хорошего дня!",
                    },
                },
            )

        return ActivateQrCodeResponseDTO.model_validate(result)

    async def all_active_tickets_event(
        self, jwt_token: str, event_id: int
    ) -> AllActiveTicketsEventResponseDTO:
        """
        Метод для получения активированных билетов мероприятия.

        Args:
            jwt_token (str): JWT токен пользователя.
            event_id (int): ID мероприятия.

        Returns:
            AllActiveTicketsEventResponseDTO (BaseModel): Возвращает пайдемик модель.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        by_type, total = await db_all_active_tickets_event(self.db, event_id)

        return AllActiveTicketsEventResponseDTO.model_validate(
            {"total": total, "by_type": by_type}
        )

    async def all_tickets_event(
        self, jwt_token: str, event_id: int
    ) -> AllTicketsEventResponseDTO:
        """
        Метод для получения всех билетов мероприятия.

        Args:
            jwt_token (str): JWT токен пользователя.
            event_id (int): ID мероприятия.

        Returns:
            AllTicketsEventResponseDTO (BaseModel): Возвращает пайдемик модель.

        Raises:
            NoTokenError: Токен неправильный/отсутствует.
        """
        if not await token_verification(jwt_token):
            raise NoTokenError()

        by_type, total = await db_all_tickets_event(self.db, event_id)

        return AllTicketsEventResponseDTO.model_validate(
            {"total": total, "by_type": by_type}
        )
