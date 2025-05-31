from typing import Any, Dict, Callable, ParamSpec, Tuple, TypeVar, Awaitable
from functools import wraps
import json
import hashlib
from dataclasses import dataclass

from fastapi.encoders import jsonable_encoder

from ..models.session import get_db
from ..models.crud import search_user
from ..security.jwt import token_verification
from ..core.exceptions import NoTokenError, TokenError
from ..schemas import IntUserId

P = ParamSpec('P')
R = TypeVar('R')

iprefix = '[ICache]'


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


@dataclass(frozen=True)
class Colors:
    """Цвета для консоли"""
    RED: str = "\033[91m"
    GREEN: str = "\033[92m"
    BLUE: str = "\033[94m"
    MAGENTA: str = "\033[35m"
    CYAN: str = "\033[36m"
    RESET: str = "\033[0m"


class LogInfo:
    """Красивый вывод логов в консоль"""

    def __init__(self, session_name: str) -> None:
        self.name = f'[{session_name}]'

    def iprint(self, text: str) -> bool:
        """
        Вывод логов в консоль.

        Args:
            text (str): Текст для вывода.

        Returns:
            bool: Произошел ли вывод.
        """
        output = f"{Colors.BLUE}{iprefix}{Colors.RESET} {Colors.CYAN}{self.name}{Colors.RESET} {text}"
        print(output)
        return True


class IClearCache:
    """Декоратор для чистки кеша"""
    loger_name = LogInfo

    def __init__(
        self,
        *,
        unique_name: str,
        jwt_token_path: None | str = None,
        add_pydantic_model: None | str = None,
        add_jwt_token: bool = False,
        add_jwt_user_id: bool = False,
    ) -> None:

        check_data = {
            unique_name: str,
            jwt_token_path: (type(None), str),
            add_pydantic_model: (type(None), str),
            add_jwt_token: bool,
            add_jwt_user_id: bool
        }
        for key, value in check_data.items():
            if not isinstance(key, value):
                text_error = f"Ошибка. {key = } должно быть {value}"
                raise ValueError(text_error)

        self.unique_name = unique_name
        self.jwt_token_path = jwt_token_path
        self.add_pydantic_model = add_pydantic_model
        self.add_jwt_token = add_jwt_token
        self.add_jwt_user_id= add_jwt_user_id

        # устанавливаем сессию логера
        self.log = self.loger_name(unique_name)

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if self.jwt_token_path is None and (self.add_jwt_token or self.add_jwt_user_id):
                raise ValueError('Вы не указали путь к токену')

            parameters = {}

            if self.jwt_token_path is not None:
                user_id, token = await valid_token_and_user_in_db(func, kwargs, self.jwt_token_path)

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
            print(key_redis)
            self.log.iprint('вот так вот')

            return await func(*args, **kwargs)

        return wrapper


class ICache:
    """Декоратор для использования кеша"""
    loger_name = LogInfo

    def __init__(
        self,
        *,
        unique_name: str,
        jwt_token_path: None | str = None,
        add_pydantic_model: None | str = None,
        add_jwt_token: bool = False,
        add_jwt_user_id: bool = False,
        time_ttl: int = 0
    ) -> None:

        check_data = {
            unique_name: str,
            jwt_token_path: (type(None), str),
            add_pydantic_model: (type(None), str),
            add_jwt_token: bool,
            add_jwt_user_id: bool,
            time_ttl: int,
        }
        for key, value in check_data.items():
            if not isinstance(key, value):
                text_error = f"Ошибка. {key = } должно быть {value}"
                raise ValueError(text_error)

        self.unique_name = unique_name
        self.jwt_token_path = jwt_token_path
        self.add_pydantic_model = add_pydantic_model
        self.add_jwt_token = add_jwt_token
        self.add_jwt_user_id= add_jwt_user_id

        if 2_147_483_647 > time_ttl > -1:
            self.time_ttl = time_ttl
        else:
            raise ValueError('Время должно быть в пределах 2_147_483_647 > time_ttl > -1')

        # устанавливаем сессию логера
        self.log = self.loger_name(unique_name)

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if self.jwt_token_path is None and (self.add_jwt_token or self.add_jwt_user_id):
                raise ValueError('Вы не указали путь к токену')

            parameters = {}

            if self.jwt_token_path is not None:
                user_id, token = await valid_token_and_user_in_db(func, kwargs, self.jwt_token_path)

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