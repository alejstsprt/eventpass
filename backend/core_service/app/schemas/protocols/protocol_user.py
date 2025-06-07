from typing import TYPE_CHECKING, Protocol

from fastapi import Response

if TYPE_CHECKING:
    from schemas import CreateUser, LoginUser, LoginUserResult, UserRegistrationResult


class ManagementUsersProtocol(Protocol):
    """Протокол ManagementUsers"""

    async def create_user(
        self, response: Response, user: "CreateUser"
    ) -> "UserRegistrationResult":
        """
        Метод для создания пользователя в базе данных.

        Args:
            response (Response): ответ, который сервер (FastAPI) отправляет клиенту
            user (LoginUser): Имя, логин и пароль.

        Returns:
            UserRegistrationResult (TypedDict): Возвращает `{'result': True, 'user_id': int}`.

        Raises:
            LoginAlreadyExistsException (HTTPException): Пользователь уже существует.
            RegistrationFailedException (HTTPException): Ошибка регистрации.
            ValidationError (HTTPException): Неверные входные данные.
            InternalServerError (HTTPException): Ошибка сервера.
        """
        ...

    async def login_user(
        self, response: Response, user: "LoginUser"
    ) -> "LoginUserResult":
        """
        Метод для входа в аккаунт.

        Args:
            user (LoginUser): Логин и пароль.
            response (Response): ответ, который сервер (FastAPI) отправляет клиенту

        Returns:
            dict: Возвращает `{'result': True, 'id': ID, 'name': Name}`.

        Raises:
            ValidationError (HTTPException): Неверные данные.
            LoginError (HTTPException): Неверный логин.
            PasswordError (HTTPException): Неверный пароль.
        """
        ...
