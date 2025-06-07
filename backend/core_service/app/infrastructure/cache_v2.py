"""
name: ICache
v: v2.0
"""

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from functools import wraps
from inspect import iscoroutinefunction
from typing import (
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Dict,
    Final,
    List,
    Literal,
    Optional,
    ParamSpec,
    Protocol,
    Self,
    Tuple,
    TypeVar,
    Union,
    runtime_checkable,
)

import redis
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from redis import Redis

P = ParamSpec("P")
R = TypeVar("R")

IPREFIX = "[ICache]"


def _create_cache_key(name: str, data: Dict[str, Any]) -> str:
    """
    Возвращает ключ для Redis.

    Args:
        name (str): Уникальное имя сессии.
        data (Dict[str, Any]): json запрос пользователя.

    Returns:
        str: Готовый ключ для Redis.
    """
    serialized_data = json.dumps(data, sort_keys=True).encode("utf-8")
    key_hash = hashlib.sha256(serialized_data).hexdigest()
    return f"name:{name}:cache:{key_hash}"


def _pydantic_transformations(
    element: Union[BaseModel, dict[str, Any], list[Any], Any]
) -> Union[dict[str, Any], list[Any], Any]:
    """Пайдемик в json"""
    try:
        return jsonable_encoder(element)
    except Exception:
        return element


async def _substitution_data(
    param: list[Any], replacement: dict[Any, Any]
) -> list[Any]:
    """
    Подмена данных.
    >>> _substitution_data(["JWT_TOKEN"], {"JWT_TOKEN": "eyJhbGciOiJIUzI1..."})
    >>> ["eyJhbGciOiJIUzI1..."]

    Args:
        param (list[Any]): Лист с данными, которые нужно заменить.
        replacement (dict[Any]): Словарь с данными для замены.

    Returns:
        list[Any]: Лист с замененными данными.
    """
    for index, elem in enumerate(param):
        if not isinstance(elem, str):
            continue

        if elem in replacement.keys():
            param[index] = _pydantic_transformations(replacement[elem])
    return param


@runtime_checkable
class ICacheWriterProtocol(Protocol):
    """
    Класс-протокол
    """

    async def __call__(self, **kwargs: object) -> Any:
        """Вызов функции"""
        ...

    def __repr__(self) -> str: ...


@runtime_checkable
class IParamProtocol(Protocol):
    """
    Класс-протокол
    """

    async def __call__(self, **injections: object) -> Any:
        """Вызов функции"""
        ...

    @staticmethod
    async def __process_args(
        param: list[Any], replacement: dict[Any, Any]
    ) -> list[Any]:
        """Функция просто делегирует"""
        ...

    @staticmethod
    async def __process_kwargs(
        param: dict[Any, Any], replacement: dict[Any, Any]
    ) -> dict[Any, Any]:
        """Подстановка данных"""
        ...

    def __repr__(self) -> str: ...


async def _launch_operation(
    functions: list[Callable[..., Any]],
    **kwargs: object,
) -> list[Any]:
    """
    Функция для запуска списка функций.

    Args:
        functions (object): Функции.
        cache_writer (object): Класс для понимания что если он есть - данные нужно кешировать.
        kwargs (object): тело оригинальной функции.

    Returns:
        list[Any]: Список результатов функций, который можно сгенерировать для ключа.
    """
    # Логика такая:
    # _launch_operation -> ICacheWriter -> IParam
    result: List[Any] = []

    for operation in functions:
        if isinstance(operation, ICacheWriterProtocol):
            result.append(await operation(**kwargs))
        elif isinstance(operation, IParamProtocol):
            await operation()
        elif iscoroutinefunction(operation):
            await operation()
        else:
            operation()

    return result


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

    HOST: Final[str] = "localhost"
    PORT: Final[int] = 6379
    DB: Final[int] = 0
    DECODE_RESPONSES: Final[bool] = True
    TIME_SAVE_NO_CONNECTING: Final[int] = (
        10  # TODO: сделать умный обход подключеня к редис если он упал
    )


class LoggerProtocol(Protocol):
    def iprint(self, text: str) -> Literal[True]:
        """
        Вывод логов в консоль.

        Args:
            text (str): Текст для вывода.
        """
        ...


class _LogInfo:
    """Красивый вывод логов в консоль"""

    def __init__(self, session_name: str) -> None:
        self.name = f"[{session_name}]"

    def iprint(self, text: str) -> Literal[True]:
        """
        Вывод логов в консоль.

        Args:
            text (str): Текст для вывода.

        Returns:
            bool: Произошел ли вывод.
        """
        output = f"{Colors.BLUE}{IPREFIX}{Colors.RESET} {Colors.CYAN}{self.name}{Colors.RESET} {text}"
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
        output = f"{Colors.BLUE}{IPREFIX}{Colors.RESET} {Colors.CYAN}{self.name}{Colors.RESET} {Colors.RED}{text}{Colors.RESET}"
        print(output)
        return True


class IParam:
    """
    Передаёт **аргументы** в функцию при вызове (но не результат!).
    Полезен, когда нужно:
    - Заранее подготовить аргументы
    - Динамически подставлять значения из контекста

    Пример 1: Базовое использование
    ```python
    def log_operation(action: str, user_id: int) -> None:
        print(f"[User {user_id}] {action}")

    @ICache(
        unique_name="user_actions",
        functions=[
            IParam(log_operation, "{action_name}", user_id=42)
        ]
    )
    ```

    Пример 2: Интеграция с FastAPI
    ```python
    @ICache(
        unique_name="ticket-types",
        functions=[
            IParam(verify_token, "auth_token")  # Автоматическая подстановка
        ]
    )
    async def get_ticket_types(
        event_id: int = Path(..., title="ID мероприятия"),
        auth_token: str = Cookie(alias="jwt_token"),  # Сюда подставится значение
        service: TicketService = Depends(get_ticket_service),
    ) -> list[TicketType]:
        return await service.get_types(event_id, auth_token)
    ```

    Как это работает:
    1. При генерации ключа кеша:
       - `"{action_name}"` → заменится на переданное значение
       - `"auth_token"` → возьмётся из параметров функции
    2. Указанная функция будет вызвана с подставленными аргументами

    **ВАЖНО:**
    - Всегда указывайте точное имя переменной в строке (например `"auth_token"`)
    """

    def __init__(
        self, func: Callable[..., Any], *args: object, **kwargs: object
    ) -> None:
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    async def __call__(self, **injections: object) -> Any:
        """Вызов функции"""
        if injections:
            args = deepcopy(self.__args)
            kwargs = deepcopy(self.__kwargs)

            if iscoroutinefunction(self.__func):
                return self.__func(
                    *await self.__process_args([*args], injections),
                    **await self.__process_kwargs(kwargs, injections),
                )

            return self.__func(
                *await self.__process_args([*args], injections),
                **await self.__process_kwargs(kwargs, injections),
            )

        if iscoroutinefunction(self.__func):
            return await self.__func(*self.__args, **self.__kwargs)
        return self.__func(*self.__args, **self.__kwargs)

    @staticmethod
    async def __process_args(
        param: list[Any], replacement: dict[Any, Any]
    ) -> list[Any]:
        """Функция просто делегирует"""
        return await _substitution_data(param, replacement)

    @staticmethod
    async def __process_kwargs(
        param: dict[Any, Any], replacement: dict[Any, Any]
    ) -> dict[Any, Any]:
        """Подстановка данных"""
        for kay, value in param.items():
            if not isinstance(value, str):
                continue

            if value in replacement.keys():
                param[kay] = replacement[value]
        return param

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(func={self.__func}, args={self.__args}, kwargs={self.__kwargs})"


class ICacheWriter:
    """
    Обёртка для функций, результат которых должен стать частью ключа кеша.

    Функция вызывается **в момент генерации ключа**.

    Пример:
    ```python
    def get_user_id():
        return current_user.id  # динамический параметр

    @ICache(
        unique_name="user_data",
        functions = [
            ICacheWriter(get_user_id) # user_id станет частью ключа
        ]
    )
    ```
    Ключ будет сгенерирован с учетом результата функции `get_user_id`. В данном случае ID пользователя.
    """

    __param = IParam

    def __init__(self, func: Callable[..., Any]) -> None:
        self.__func = func

    async def __call__(self, **kwargs: object) -> Any:
        """Вызов функции"""
        # Вызов функции ICacheWriter(func)
        # Если это IParam, то вызываем и передаем туда тело оригинальной функции, чтобы заменить строки на реальные данные
        if isinstance(self.__func, self.__param):
            return await self.__func(**kwargs)

        if iscoroutinefunction(self.__func):
            return await self.__func()
        return self.__func()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(func={self.__func})"


class _RedisService:
    """Управление редисом"""

    __instance: ClassVar[Self | None] = None
    redis: Redis

    def __new__(cls, logger: LoggerProtocol, *args: object, **kwargs: object) -> Self:
        if not hasattr(logger, "iprint") or not callable(logger.iprint):
            raise AttributeError('Логгер не имеет метода "iprint(text: str)') from None

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            logger.iprint("Подключение к Redis...")
            cls.__connect_redis()
            logger.iprint("Подключено")
            return cls.__instance
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
        if cls.__instance is None:
            raise RuntimeError("Экземпляр RedisService не был создан") from None
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
            raise ConnectionError("Ошибка подключения к Redis") from None

    def search_key(self, cache: str) -> Any:
        """
        Метод для поиска кеша в Redis.

        Args:
            cache (str): Кеш-ключ.

        Returns:
            Any: Результат поиска.
        """
        return self.redis.get(cache)

    def save_key(self, cache: str, value: Dict[str, Any], time: int) -> Any:
        """
        Метод для сохранения кеша в Redis.

        Args:
            cache (str): Кеш-ключ.
            value (Dict[str, Any]): Данные-значение.
            time (int): Время жизни кеша. `time=0` - бесконечно.

        Returns:
            Any: Результат сохранения.
        """
        if time:
            return self.redis.setex(cache, time, str(value))
        return self.redis.set(cache, str(value))

    def delete_key(self, cache: str) -> Any:
        """
        Метод для удаления кеша Redis.

        Args:
            cache (str): Кеш-ключ.

        Returns:
            Any: Результат удаления.
        """
        return self.redis.delete(cache)


class IClearCache:
    """Декоратор для чистки кеша"""

    __loger_name = _LogInfo
    __redis_name = _RedisService

    def __init__(
        self,
        *,
        unique_name: str,
        functions: Optional[list[Callable[..., Any]]] = None,
        data: Optional[list[Any]] = None,
        time_ttl: int = 0,
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
        self.unique_name = unique_name
        self.functions = functions
        self.data = data

        if 2_147_483_647 > time_ttl > -1:
            self.time_ttl = time_ttl
        else:
            raise ValueError(
                "Время должно быть в пределах 2_147_483_647 > time_ttl > -1"
            )

        # устанавливаем сессию логера и редис
        self.log = self.__loger_name(unique_name)
        self.redis = self.__redis_name(self.log)

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """Вызов функции"""

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            parameters: dict[str, Any] = {}

            if self.functions:
                functions = deepcopy(self.functions)

                if func_result := await _launch_operation(functions, **kwargs):
                    parameters["__ifunc__"] = func_result

            if self.data:
                data = deepcopy(self.data)

                if data_result := await _substitution_data(data, kwargs):
                    parameters["__idata__"] = data_result

            key_redis: str = _create_cache_key(self.unique_name, parameters)
            self.log.iprint(f"{parameters} | {key_redis}")

            return await self.__interaction_redis(key_redis, func, *args, **kwargs)

        return wrapper

    async def __interaction_redis(
        self,
        key_redis: str,
        func: Callable[..., Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> R:
        """Работа с редис"""
        try:
            if self.redis.search_key(key_redis) is not None:
                self.redis.delete_key(key_redis)
                self.log.iprint("Кеш удален")
        except redis.ConnectionError as e:
            self.log.ierror(f"Не удалось удалить кеш. {e}")

        return await func(*args, **kwargs)


class ICache:
    """Декоратор для использования кеша"""

    __loger_name = _LogInfo
    __redis_name = _RedisService

    def __init__(
        self,
        *,
        unique_name: str,
        functions: Optional[list[Callable[..., Any]]] = None,
        data: Optional[list[Any]] = None,
        time_ttl: int = 0,
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
        self.unique_name = unique_name
        self.functions = functions
        self.data = data

        if 2_147_483_647 > time_ttl > -1:
            self.time_ttl = time_ttl
        else:
            raise ValueError(
                "Время должно быть в пределах 2_147_483_647 > time_ttl > -1"
            )

        # устанавливаем сессию логера и редис
        self.log = self.__loger_name(unique_name)
        self.redis = self.__redis_name(self.log)

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """Вызов функции"""

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            parameters: dict[str, Any] = {}

            if self.functions:
                functions = deepcopy(self.functions)

                if func_result := await _launch_operation(functions, **kwargs):
                    parameters["__ifunc__"] = func_result

            if self.data:
                data = deepcopy(self.data)

                if data_result := await _substitution_data(data, kwargs):
                    parameters["__idata__"] = data_result

            key_redis: str = _create_cache_key(self.unique_name, parameters)
            self.log.iprint(f"{parameters} | {key_redis}")

            return await self.__interaction_redis(key_redis, func, *args, **kwargs)

        return wrapper

    async def __interaction_redis(
        self,
        key_redis: str,
        func: Callable[..., Any],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Callable[..., Any]:
        """Работа с редис"""
        try:
            if self.redis.search_key(key_redis) is None:
                result = await func(*args, **kwargs)
                json_value = jsonable_encoder(result)

                self.redis.save_key(key_redis, json_value, self.time_ttl)

                self.log.iprint("Кеш сохранен")
                return result
            else:
                json_str = self.redis.search_key(key_redis)
                fixed_json = json_str.replace("'", '"')
                json_result: R = json.loads(fixed_json)

                self.log.iprint("Кеш использован")
                return json_result
        except redis.ConnectionError as e:
            self.log.ierror(f"Не удалось использовать кеш. {e}")
            return await func(*args, **kwargs)
