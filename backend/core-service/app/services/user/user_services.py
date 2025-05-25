from sqlalchemy.orm import Session
from fastapi import Response

from ...schemas.user import CreateUser, LoginUser
from ...models.crud import user_registration, search_user
from ...security.hashing import hash_password, verify_password
from ...security.jwt import set_jwt_cookie, create_access_token
from ...core.exceptions import (
    LoginAlreadyExistsException,
    ValidationError,
    PasswordError,
    LoginError,
    InternalServerError
)


class ManagementUsers:
    """
    Модуль для управления пользователем.
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, response: Response, user: CreateUser) -> dict:
        """
        Метод для создания пользователя в базе данных

        Args:
            - user (LoginUser): Имя, логин и пароль.
            - response (Response)

        Returns:
            - `{'result': True}`

        Raises:
            - `LoginAlreadyExistsException` (HTTPException): Пользователь уже существует.
            - `RegistrationFailedException` (HTTPException): Ошибка регистрации.
        """
        if not user.name or not user.login or not user.password:
            raise ValidationError()

        hash_pass = hash_password(user.password)
        result = await user_registration(self.db, user.name, user.login, hash_pass)

        if result['result']:
            token = await create_access_token(result['user_id'])
            await set_jwt_cookie(response, token)
            return result

        elif result['error'] != 'Ошибка сервера':
            raise LoginAlreadyExistsException()

        else:
            raise InternalServerError()

    async def login_user(self, response: Response, user: LoginUser) -> dict:
        """
        Метод для входа в аккаунт.

        Args:
            - user (LoginUser): Логин и пароль.
            - response (Response)

        Returns:
            - `{'result': True, 'id': ID, 'name': Name}` (dict): Успешный вход.
        Raises:
            - `ValidationError` (HTTPException). Неверные данные.
            - `LoginError` (HTTPException). Неверный логин.
            - `PasswordError` (HTTPException). Неверный пароль.
        """
        if not self.db or not user.login or not user.password:
            raise ValidationError()

        db_user = await search_user(self.db, login=user.login)
        db_user = db_user['login']
        if not db_user:
            raise LoginError()

        is_password = verify_password(user.password, db_user.password_hash)
        if not is_password:
            raise PasswordError()

        token = await create_access_token(db_user.id)
        await set_jwt_cookie(response, token)

        return {'id': db_user.id, 'name': db_user.name}