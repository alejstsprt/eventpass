from typing import Union

from sqlalchemy.orm import Session

from ...schemas.user import CreateUser, LoginUser
from ...models.crud import user_registration
from ...models.models import Accounts, Events, TicketTypes, Tickets
from ...core.exceptions import LoginAlreadyExistsException, RegistrationFailedException, ValidationError
from ...security.hashing import hash_password, verify_password


class ManagementUsers:
    """Модуль для управления пользователем пользователем.

    `create_user(user: LoginUser)` - создать пользователя
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user: CreateUser) -> dict:
        """
        Метод для создания пользователя в базе данных

        Args:
            - user (LoginUser): Имя, логин и пароль.

        Returns:
            - `{'result': True}`

        Raises:
            - `LoginAlreadyExistsException` (HTTPException): Пользователь уже существует.
            - `RegistrationFailedException` (HTTPException): Ошибка регистрации.
        """
        if not user.name or not user.login or not user.password:
            raise RegistrationFailedException()

        hash_pass = hash_password(user.password)
        result = await user_registration(self.db, user.name, user.login, hash_pass)

        if result['result']:
            return {'result': True}
        elif result['error'] != 'Ошибка сервера':
            raise LoginAlreadyExistsException()
        else:
            raise RegistrationFailedException()

    async def login_user(self, user: LoginUser) -> dict:
        """
        Метод для входа в аккаунт

        Args:
            - user (LoginUser): Логин и пароль.

        Returns:
            - `{'result': True, 'id': ID, 'name': Name}` (dict): Успешный вход.
            - `{'result': False, 'error': Error}` (dict): Логин/пароль неверный.
        Raises:
            - `ValidationError` (HTTPException). Неверные данные
        """
        if not self.db or not user.login or not user.password:
            raise ValidationError()

        db_user = self.db.query(Accounts).filter(Accounts.login == user.login).first()
        if not db_user:
            return {'result': False, 'error': 'Неверный логин'}

        is_password = verify_password(user.password, db_user.password_hash)
        if not is_password:
            return {'result': False, 'error': 'Неверный пароль'}

        return {'result': True, 'id': db_user.id, 'name': db_user.name}