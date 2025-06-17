from typing import TYPE_CHECKING, Protocol

from fastapi import Response

if TYPE_CHECKING:
    from infrastructure.messaging.producer import RabbitProducer
    from schemas import (
        CreateUserDTO,
        CreateUserResponseDTO,
        GetUserInfoResponseDTO,
        LoginUserDTO,
        LoginUserResponseDTO,
    )


class ManagementUsersProtocol(Protocol):
    """Протокол ManagementUsers"""

    async def create_user(
        self,
        response: Response,
        user: "CreateUserDTO",
        rabbit_producer: "RabbitProducer",
    ) -> "CreateUserResponseDTO":
        """
        Метод для создания пользователя в базе данных.

        Args:
            response (Response): ответ, который сервер (FastAPI) отправляет клиенту
            user (LoginUser): Имя, логин и пароль.

        Returns:
            CreateUserResponseDTO (BaseModel): Возвращает пайдемик модель ответа.

        Raises:
            LoginAlreadyExistsException (HTTPException): Пользователь уже существует.
            RegistrationFailedException (HTTPException): Ошибка регистрации.
            ValidationError (HTTPException): Неверные входные данные.
            InternalServerError (HTTPException): Ошибка сервера.
        """
        ...

    async def login_user(
        self, response: Response, user: "LoginUserDTO"
    ) -> "LoginUserResponseDTO":
        """
        Метод для входа в аккаунт.

        Args:
            user (LoginUser): Логин и пароль.
            response (Response): ответ, который сервер (FastAPI) отправляет клиенту

        Returns:
            LoginUserResponseDTO (BaseModel): Возвращает пайдемик модель ответа.

        Raises:
            ValidationError (HTTPException): Неверные данные.
            LoginError (HTTPException): Неверный логин.
            PasswordError (HTTPException): Неверный пароль.
        """
        ...

    async def get_info_user(self, jwt_token: str) -> "GetUserInfoResponseDTO":
        """
        Метод возвращает информацию о пользователе из токена.

        Args:
            jwt_token (str): JWT токен пользователя.

        Raises:
            NoTokenError: Токен отсутствует/неверный.

        Returns:
            GetUserInfoResponseDTO (BaseModel): Возвращает пайдемик модель ответа.
        """
        ...
