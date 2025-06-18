from typing import TYPE_CHECKING

from fastapi import Response
from sqlalchemy.orm import Session

from core.config import config
from core.exceptions import LoginError, NoTokenError, PasswordError
from models.crud import db_get_info_user, search_user, user_registration
from schemas import (
    CreateUserResponseDTO,
    GetUserInfoResponseDTO,
    LoginUserResponseDTO,
    StrUserLogin,
    StrUserName,
    StrUserPassword,
)
from security.hashing import hash_password, verify_password
from security.jwt import create_access_token, set_jwt_cookie, token_verification

if TYPE_CHECKING:
    from infrastructure.messaging.producer import RabbitProducer
    from schemas import CreateUserDTO, LoginUserDTO, StrUserLogin


class ManagementUsers:
    """
    Модуль для управления пользователем.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_user(
        self,
        response: Response,
        user: "CreateUserDTO",
        rabbit_producer: "RabbitProducer",
    ) -> CreateUserResponseDTO:
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
        hash_pass = hash_password(user.password)
        result = await user_registration(
            self.db,
            StrUserName(user.name),
            StrUserLogin(user.login),
            StrUserPassword(hash_pass),
        )
        token = await create_access_token(result.id)
        await set_jwt_cookie(response, token)

        await rabbit_producer.add_to_queue(
            config.QUEUE_NAME,
            {
                "type": "email",
                "payload": {
                    "to": f"{result.login}",
                    "title": "Спасибо за регистрацию",
                    "text": f"{result.name}, благодарим вас за регистрацию на нашем сайте!",
                },
            },
        )
        return CreateUserResponseDTO.model_validate(result)

    async def login_user(
        self, response: Response, user: "LoginUserDTO"
    ) -> LoginUserResponseDTO:
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
        user_data = await search_user(self.db, login=StrUserLogin(user.login))
        db_user = user_data["login"]
        if not db_user:
            raise LoginError()

        is_password = verify_password(user.password, str(db_user.password_hash))
        if not is_password:
            raise PasswordError()

        token = await create_access_token(db_user.id)
        await set_jwt_cookie(response, token)

        return LoginUserResponseDTO.model_validate(db_user)

    async def get_info_user(self, jwt_token: str) -> GetUserInfoResponseDTO:
        """
        Метод возвращает информацию о пользователе из токена.

        Args:
            jwt_token (str): JWT токен пользователя.

        Raises:
            NoTokenError: Токен отсутствует/неверный.

        Returns:
            GetUserInfoResponseDTO (BaseModel): Возвращает пайдемик модель ответа.
        """
        user_id = await token_verification(jwt_token)

        if not user_id:
            raise NoTokenError()

        result = await db_get_info_user(self.db, user_id)

        return GetUserInfoResponseDTO.model_validate(result)
