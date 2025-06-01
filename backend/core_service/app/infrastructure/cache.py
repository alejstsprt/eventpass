from typing import Any, Dict, Callable, ParamSpec, Tuple, TypeVar, Awaitable, Self, Literal, Final
from dataclasses import dataclass
from functools import wraps
import hashlib
import json

from fastapi.encoders import jsonable_encoder
from redis import Redis
import redis

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
    Возвращает ключ для Redis.

    Args:
        name (str): Уникальное имя сессии.
        data (Dict[str, Any]): json запрос пользователя.

    Returns:
        str: Готовый ключ для Redis.
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
        try:
            if (result_search_token := kwargs[jwt_token_path]) is None:
                raise NoTokenError()
        except KeyError:
            error = f"Неверный путь к токену ({jwt_token_path} not in {func.__name__})"
            raise ValueError(error)

        if (result_search_user_id := await token_verification(result_search_token)) is None:
            raise TokenError()

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
    RED: Final[str] = "\033[91m"
    GREEN: Final[str] = "\033[92m"
    BLUE: Final[str] = "\033[94m"
    MAGENTA: Final[str] = "\033[35m"
    CYAN: Final[str] = "\033[36m"
    RESET: Final[str] = "\033[0m"


@dataclass(frozen=True)
class SettingsRedis:
    """Настройки Redis"""
    HOST: Final[str] = 'localhost'
    PORT: Final[int] = 6379
    DB: Final[int] = 0
    DECODE_RESPONSES: Final[bool] = True
    TIME_SAVE_NO_CONNECTING: Final[int] = 10 # TODO: сделать умный обход подключеня к редис если он упал


class LogInfo:
    """Красивый вывод логов в консоль"""

    def __init__(self, session_name: str) -> None:
        self.name = f'[{session_name}]'

    def iprint(self, text: str) -> Literal[True]:
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

    def ierror(self, text: str) -> Literal[True]:
        """
        Вывод логов в консоль.

        Args:
            text (str): Текст для вывода.

        Returns:
            bool: Произошел ли вывод.
        """
        output = f"{Colors.BLUE}{iprefix}{Colors.RESET} {Colors.CYAN}{self.name}{Colors.RESET} {Colors.RED}{text}{Colors.RESET}"
        print(output)
        return True


class RedisService:
    """Управление редисом"""
    __instance: Self | None = None
    redis: Redis

    def __new__(cls, *args: P.args, **kwargs: P.kwargs) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__connect_redis()
            return cls.__instance
        else:
           return cls.__instance 

    @classmethod
    def __connect_redis(cls) -> Literal[True]:
        """
        Устанавливаем соединение.

        Raises:
            ConnectionError: не удалось подключиться к Redis.

        Returns:
            Literal[True]: Соединение установлено.
        """
        try:
            cls.__instance.redis = Redis(
                host=SettingsRedis.HOST,
                port=SettingsRedis.PORT,
                db=SettingsRedis.DB,
                decode_responses=SettingsRedis.DECODE_RESPONSES,
            )
            cls.__instance.redis.ping()
            return True
        except Exception as e:
            raise ConnectionError('Ошибка подключения к Redis')

    def search_key(self, cache: str) -> Dict[str, Any] | None:
        """
        Метод для поиска кеша в Redis.

        Args:
            cache (str): Кеш-ключ.

        Returns:
            Dict[str, Any] | None: Результат поиска.
        """
        return self.redis.get(cache)

    def save_key(self, cache: str, value: Dict[str, Any], time: int) -> bool:
        """
        Метод для сохранения кеша в Redis.

        Args:
            cache (str): Кеш-ключ.
            value (Dict[str, Any]): Данные-значение.
            time (int): Время жизни кеша. `time=0` - бесконечно.

        Returns:
            bool: Результат сохранения.
        """
        if time:
            return self.redis.setex(cache, time, str(value))
        return self.redis.set(cache, str(value))

    def delete_key(self, cache: str) -> bool:
        """
        Метод для удаления кеша Redis.

        Args:
            cache (str): Кеш-ключ.

        Returns:
            bool: Результат удаления.
        """
        return self.redis.delete(cache)


class IClearCache:
    """Декоратор для чистки кеша"""
    loger_name = LogInfo
    redis_name = RedisService

    def __init__(
        self,
        *,
        unique_name: str,
        jwt_token_path: str | None = None,
        add_pydantic_model: str | None = None,
        add_jwt_token: bool = False,
        add_jwt_user_id: bool = False,
    ) -> None:
        """
        Декоратор для очистки кеша. Полезен, чтобы не выдавало старых данных.

        Args:
            unique_name (str): Уникальное имя сессии кеша.
            jwt_token_path (str | None, optional): Путь к токену. `Декоратор сам проверяет токен и есть ли user в db`. Defaults to None.
            add_pydantic_model (str | None, optional): Путь к pydantic модели. Defaults to None.
            add_jwt_token (bool, optional): Добавить ли токен в кеш. Defaults to False.
            add_jwt_user_id (bool, optional): Добавить ли айди из токена в кеш. Defaults to False.

        Raises:
            ValueError: Неверные входные данные.
        """

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

        # устанавливаем сессию логера и редис
        self.log = self.loger_name(unique_name)
        self.redis = self.redis_name()

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

            try:
                # Временная заглуша вместо Редиса
                if self.redis.search_key(key_redis) is not None:
                    self.redis.delete_key(key_redis)
                    self.log.iprint('Кеш удален')
            except redis.ConnectionError as e:
                self.log.ierror(f'Не удалось удалить кеш. {e}')

            return await func(*args, **kwargs)

        return wrapper


class ICache:
    """Декоратор для использования кеша"""
    loger_name = LogInfo
    redis_name = RedisService

    def __init__(
        self,
        *,
        unique_name: str,
        jwt_token_path: str | None = None,
        add_pydantic_model: str | None = None,
        add_jwt_token: bool = False,
        add_jwt_user_id: bool = False,
        time_ttl: int = 0
    ) -> None:
        """
        Декоратор для использования кеша. Полностью сохраняет результат и переиспользует.

        Args:
            unique_name (str): Уникальное имя сессии кеша.
            jwt_token_path (str | None, optional): Путь к токену. `Декоратор сам проверяет токен и есть ли user в db`. Defaults to None.
            add_pydantic_model (str | None, optional): Путь к pydantic модели. Defaults to None.
            add_jwt_token (bool, optional): Добавить ли токен в кеш. Defaults to False.
            add_jwt_user_id (bool, optional): Добавить ли айди из токена в кеш. Defaults to False.
            time_ttl (int, optional): Время жизни кеша. По умолчанию бесконечное. Defaults to 0.

        Raises:
            ValueError: Неверные входные данные.
        """

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

        # устанавливаем сессию логера и редис
        self.log = self.loger_name(unique_name)
        self.redis = self.redis_name()

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

            try:
                if self.redis.search_key(key_redis) is None:
                    result = await func(*args, **kwargs)
                    json_value = jsonable_encoder(result)

                    self.redis.save_key(key_redis, json_value, self.time_ttl)

                    self.log.iprint('Кеш сохранен')
                    return result
                else:
                    json_str = self.redis.search_key(key_redis)
                    fixed_json = json_str.replace("'", '"')

                    self.log.iprint('Кеш использован')
                    return json.loads(fixed_json)
            except redis.ConnectionError as e:
                self.log.ierror(f'Не удалось использовать кеш. {e}')
                return await func(*args, **kwargs)
        return wrapper
