from functools import wraps
import json
import hashlib
from typing import Any, Dict, Callable, ParamSpec, Tuple, TypeVar, Awaitable

from fastapi.encoders import jsonable_encoder

from ..models.session import get_db
from ..models.crud import search_user
from ..security.jwt import token_verification
from ..core.exceptions import NoTokenError, TokenError
from ..schemas import IntUserId

P = ParamSpec('P')
R = TypeVar('R')


def create_cache_key(name: str, data: Dict[str, Any]) -> str:
    """
    Возвращает ключ для Redis

    Args:
        name (str): Уникальное имя сессии.
        data (Dict[str, Any]): json запрос пользователя.

    Returns:
        str: Готовый ключ для Redis
    """
    serialized_data = json.dumps(data, sort_keys=True).encode('utf-8')
    key_hash = hashlib.sha256(serialized_data).hexdigest()
    return f"name:{name}:cache:{key_hash}"

class IClearCache:
    def __init__(
        self,
        *,
        unique_name: None | str,
        jwt_token: None | str = None,
        jwt_token_id: None | str = None
    ) -> None:
        self.unique_name = unique_name
        self.jwt_token = jwt_token
        self.jwt_token_id = jwt_token_id

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print(f"Входной запрос от {self.unique_name}")
            result = await func(*args, **kwargs)
            print(f'Результат: {result}')
            return result
        return wrapper


class ICache:
    def __init__(
        self,
        *,
        unique_name: None | str,
        jwt_token_path: None | str = None,
        add_pydantic_model: None | str = None,
        add_jwt_token: None | bool = False,
        add_jwt_user_id: None | bool = False,
        time_ttl: None | int = 0
    ) -> None:
        self.unique_name = unique_name
        self.jwt_token_path = jwt_token_path
        self.add_pydantic_model = add_pydantic_model
        self.add_jwt_token = add_jwt_token
        self.add_jwt_user_id= add_jwt_user_id
        self.time_ttl = time_ttl

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if self.jwt_token_path is None and (self.add_jwt_token or self.add_jwt_user_id):
                raise ValueError('Вы не указали путь к токену')

            parameters = {}

            if self.jwt_token_path is not None:
                user_id, token = await self.valid_token_and_user_in_db(func, kwargs, self.jwt_token_path)

            if self.add_jwt_token:
                parameters['user_id'] = user_id

            if self.add_jwt_user_id:
                parameters['jwt_token'] = token

            if self.add_pydantic_model is not None:
                if (result_search_pydantic_model := kwargs.get(self.add_pydantic_model)) is None:
                    error = f"Неверный путь к pydantic модели ({self.add_pydantic_model} not in {func.__name__})"
                    raise ValueError(error)
                parameters.update(jsonable_encoder(result_search_pydantic_model))

            key_redis = create_cache_key(self.unique_name, parameters)

            # Временная заглуша вместо Редиса
            if False:
                result = await func(*args, **kwargs)
                json_value = jsonable_encoder(result)
                return result
            else:
                return key_redis
        return wrapper

    @staticmethod
    async def valid_token_and_user_in_db(func: Callable[..., Any], kwargs: Dict[str, Any], jwt_token_path: str) -> Tuple[IntUserId, str]:
        """
        Метод для проверки JWT токена.

        Args:
            func (Callable[..., Any]): Функция передаваемая в декоратор.
            kwargs (Dict[str, Any]): Весь запрос пользователя.
            jwt_token_path (str): Путь к JWT токену.

        Raises:
            ValueError (Exception): Неверные данные.
            NoTokenError (HTTPException): Токен отсутствует.
            TokenError (HTTPException): Неверный токен.

        Returns:
            (Tuple[IntUserId, str]): Айди пользователя и JWT токен.
        """
        if (result_search_token := kwargs.get(jwt_token_path)) is None:
            error = f"Неверный путь к токену ({jwt_token_path} not in {func.__name__})"
            raise ValueError(error)

        if (result_search_user_id := await token_verification(result_search_token)) is None:
            raise NoTokenError()

        # Делаем сессию БД и проверяем данные токена
        db_gen = get_db()
        db = next(db_gen)
        try:
            user_info = await search_user(db, user_id=result_search_user_id)
            if user_info['id'] is None:
                raise TokenError()

            user_id = jsonable_encoder(user_info['id'])['id']
        finally:
            db_gen.close()

        return IntUserId(user_id), result_search_token