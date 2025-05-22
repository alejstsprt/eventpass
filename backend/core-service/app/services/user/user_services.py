from typing import Union

from sqlalchemy.orm import Session

from ...schemas.user import LoginUser
from ...models.crud import is_exists_login, user_registration
from ...core.exceptions import LoginAlreadyExistsException, RegistrationFailedException
from ...security.hashing import hash_password


class ManagementUsers:
    """Модуль для управления пользователем пользователем.

    `create_user(user: LoginUser)` - создать пользователя
    """

    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user: LoginUser) -> Union[dict, LoginAlreadyExistsException, RegistrationFailedException]:
        """Метод для создания пользователя в базе данных

        Args:
            - user (LoginUser): Логин и пароль.

        Returns:
            - `{'result': True}`

        Raises:
            - `LoginAlreadyExistsException` (HTTPException). Пользователь уже существует
            - `RegistrationFailedException` (HTTPException). Ошибка регистрации
        """
        is_user = await is_exists_login(self.db, user.login)
        if is_user['result']:
            raise LoginAlreadyExistsException()

        hash_pass = hash_password(user.password)
        result = await user_registration(self.db, user.login, hash_pass)
        if result['result']:
            return {'result': True}
        else:
            raise RegistrationFailedException()