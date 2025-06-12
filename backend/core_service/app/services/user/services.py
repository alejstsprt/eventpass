from typing import TYPE_CHECKING

from fastapi import Response
from models.crud import search_user, user_registration
from sqlalchemy.orm import Session

from core.exceptions import LoginError, PasswordError
from schemas import StrUserLogin, StrUserName, StrUserPassword
from security.hashing import hash_password, verify_password
from security.jwt import create_access_token, set_jwt_cookie

if TYPE_CHECKING:
    from schemas import (
        CreateUser,
        LoginUser,
        LoginUserResult,
        StrUserLogin,
        UserRegistrationResult,
    )


class ManagementUsers:
    """
    Модуль для управления пользователем.
    """

    def __init__(self, db: Session):
        self.db = db

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
        hash_pass = hash_password(user.password)
        result = await user_registration(
            self.db,
            StrUserName(user.name),
            StrUserLogin(user.login),
            StrUserPassword(hash_pass),
        )

        token = await create_access_token(result["user_id"])
        await set_jwt_cookie(response, token)
        return result

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
        user_data = await search_user(self.db, login=StrUserLogin(user.login))
        db_user = user_data["login"]
        if not db_user:
            raise LoginError()

        is_password = verify_password(user.password, str(db_user.password_hash))
        if not is_password:
            raise PasswordError()

        token = await create_access_token(db_user.id)
        await set_jwt_cookie(response, token)

        return {"id": db_user.id, "name": db_user.name}
