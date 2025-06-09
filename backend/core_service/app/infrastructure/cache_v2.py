"""
name: ICache
v: v2.0
"""

import asyncio
import hashlib
import json
import logging
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache, wraps
from inspect import getmembers, iscoroutinefunction, isfunction, signature
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

IPREFIX: Final[str] = "[ICache]"
LIMIT_TIME_REDIS: Final[int] = 2_147_483_647


def add_class_marker(**attrs):
    """Добавление атрибутов в класс"""

    def wrapper(cls):
        for key, value in attrs.items():
            setattr(cls, key, value)
        return cls

    return wrapper


def _pydantic_transformations(
    element: Union[BaseModel, dict[str, Any], list[Any], Any]
) -> Union[dict[str, Any], list[Any], Any]:
    """Пайдемик в json"""
    try:
        return jsonable_encoder(element)
    except Exception:
        return element


def _substitution_data(param: list[Any], replacement: dict[Any, Any]) -> list[Any]:
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

        if elem in replacement:
            param[index] = _pydantic_transformations(replacement[elem])
    return param


async def _launch_operation(
    functions: list[Callable[..., Any]],
    injections: dict[Any, Any],
) -> list[Any]:
    """
    Запускает список операций с автоматическим определением их типа.

    Args:
        functions: Список операций (функции, корутины или маркированные объекты).
        injections: Аргументы для дальнейшей обработки менеджерами.

    Returns:
        Список результатов выполнения операций.

    Raises:
        TypeError: Если передан невызываемый объект.
    """
    # WORK:
    # _launch_operation (обработчик и активатор)
    #   -> ICacheWriter (менеджер добавления в кеш данных)
    #   -> IParam (менеджер запуска объекта с входными данными)
    result: List[Any] = []

    for operation in functions:
        if not callable(operation):
            raise TypeError(f"объект '{operation!r}' не является вызываемым")

        class_marker = getattr(operation, "_class_marker", None)

        if class_marker == "__icachewriter__":
            result.append(await operation(injections))
        elif class_marker == "__iparam__":
            await operation(injections)
        elif iscoroutinefunction(operation):
            await operation()
        else:
            operation()

    return result


@dataclass(frozen=True)
class _Colors:
    """Цвета для консоли"""

    RED: Final[str] = "\033[91m"
    GREEN: Final[str] = "\033[92m"
    BLUE: Final[str] = "\033[94m"
    MAGENTA: Final[str] = "\033[35m"
    CYAN: Final[str] = "\033[36m"
    RESET: Final[str] = "\033[0m"


@dataclass(frozen=True)
class _SettingsRedis:
    """Настройки Redis"""

    HOST: Final[str] = "localhost"
    PORT: Final[int] = 6379
    DB: Final[int] = 0
    DECODE_RESPONSES: Final[bool] = True
    TIME_SAVE_NO_CONNECTING: Final[int] = (
        10  # TODO: сделать умный обход подключеня к редис если он упал
    )


class _LogInfo:
    """Система логов"""

    def __init__(self, session_name: str) -> None:
        self.name = f"[{session_name}]"
        self.logger = logging.getLogger(session_name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            # f"{_Colors.BLUE}%(asctime)s{_Colors.RESET} "
            # f"{_Colors.BLUE}{IPREFIX}{_Colors.RESET} {_Colors.CYAN}{self.name}{_Colors.RESET} "
            f"{_Colors.GREEN}%(levelname)s{_Colors.RESET} - %(message)s",
            # datefmt="%H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def iprint(self, text: str, prefix: bool = False) -> Literal[True]:
        """
        Вывод логов в консоль.

        Args:
            text (str): Текст для вывода.

        Returns:
            bool: Произошел ли вывод.
        """
        # output = f"{_Colors.BLUE}{IPREFIX}{_Colors.RESET} {_Colors.CYAN}{self.name}{_Colors.RESET} {text}"
        self.logger.info(text)
        return True

    def ierror(self, text: str) -> Literal[True]:
        """
        Вывод логов в консоль.

        Args:
            text (str): Текст для вывода.

        Returns:
            bool: Произошел ли вывод.
        """
        # output = f"{_Colors.BLUE}{IPREFIX}{_Colors.RESET} {_Colors.CYAN}{self.name}{_Colors.RESET} {_Colors.RED}{text}{_Colors.RESET}"
        self.logger.info(text)
        return True


@add_class_marker(_class_marker="__iparam__")
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
        auth_token: str = Cookie(None),
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
    - Всегда указывайте точное имя переменной (например `"auth_token"`)
    """

    def __init__(
        self, func: Callable[..., Any], *args: object, **kwargs: object
    ) -> None:
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs

    async def __call__(
        self, injections: object = None, *, recursion: list[Any] | None = None
    ) -> Any:
        """Вызов функции"""
        # print('>>>', self.__args)
        for arg in self.__args:
            print("ПРОБЕЖКА:", arg)
            if not getattr(arg, "_class_marker", None) == "__iparam__":
                continue

            if not recursion:
                massiv_func = []
                massiv_func = await arg(recursion=massiv_func)
                print("=========", massiv_func)
            else:
                result = await arg(recursion=massiv_func)
                massiv_func.append(result)
                return massiv_func

        if injections:
            args = deepcopy(self.__args)
            kwargs = deepcopy(self.__kwargs)

            if iscoroutinefunction(self.__func):
                return self.__func(
                    *self.__process_args([*args], injections),
                    **self.__process_kwargs(kwargs, injections),
                )

            return self.__func(
                *self.__process_args([*args], injections),
                **self.__process_kwargs(kwargs, injections),
            )

        if iscoroutinefunction(self.__func):
            return await self.__func(*self.__args, **self.__kwargs)
        return self.__func(*self.__args, **self.__kwargs)

    @staticmethod
    def __process_args(param: list[Any], replacement: dict[Any, Any]) -> list[Any]:
        """Функция просто делегирует"""
        return _substitution_data(param, replacement)

    @staticmethod
    def __process_kwargs(
        param: dict[Any, Any], replacement: dict[Any, Any]
    ) -> dict[Any, Any]:
        """Подстановка данных"""
        for kay, value in param.items():
            if not isinstance(value, str):
                continue

            if value in replacement:
                param[kay] = replacement[value]
        return param

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(func={self.__func}, args={self.__args}, kwargs={self.__kwargs})"


@add_class_marker(_class_marker="__icachewriter__")
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

    async def __call__(self, kwargs: object) -> Any:
        """Вызов функции"""
        # Вызов функции ICacheWriter(func)
        # Если это IParam, то вызываем и передаем туда тело оригинальной функции, чтобы заменить строки на реальные данные
        if isinstance(self.__func, self.__param):
            return await self.__func(kwargs)

        if iscoroutinefunction(self.__func):
            return await self.__func()
        return self.__func()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(func={self.__func})"


@runtime_checkable
class LoggerProtocol(Protocol):
    def iprint(self, text: str) -> Literal[True]:
        """
        Вывод логов в консоль.

        Args:
            text (str): Текст для вывода.
        """
        ...


class _RedisService:
    """Управление редисом"""

    __instance: ClassVar[Self | None] = None
    redis: Redis

    def __new__(cls, logger: LoggerProtocol, *args: object, **kwargs: object) -> Self:
        if not isinstance(logger, LoggerProtocol):
            raise TypeError(
                f"Класс должен иметь методы: {[name for name, _ in getmembers(LoggerProtocol, isfunction) if name != '__subclasshook__']}"
            )

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
                host=_SettingsRedis.HOST,
                port=_SettingsRedis.PORT,
                db=_SettingsRedis.DB,
                decode_responses=_SettingsRedis.DECODE_RESPONSES,
            )
            cls.__instance.redis.ping()
            return True
        except Exception as e:
            raise ConnectionError("Ошибка подключения к Redis") from None

    @classmethod
    def search_key(cls, cache: str) -> Any:
        """
        Метод для поиска кеша в Redis.

        Args:
            cache (str): Кеш-ключ.

        Returns:
            Any: Результат поиска.
        """
        return cls.__instance.redis.get(cache)

    @classmethod
    def all_keys(cls) -> list[Any, Any]:
        return cls.__instance.redis.keys()

    @classmethod
    def save_key(cls, cache: str, value: Dict[str, Any], time: int) -> Any:
        """
        Метод для сохранения кеша в Redis.

        Args:
            cache (str): Кеш-ключ.
            value (Dict[str, Any]): Данные-значение.
            time (int): Время жизни кеша. `time=0` - бесконечно.

        Returns:
            Any: Результат сохранения.
        """
        if time != -1:
            return cls.__instance.redis.setex(cache, time, str(value))
        return cls.__instance.redis.set(cache, str(value))

    @classmethod
    def delete_key(cls, cache: str) -> Any:
        """
        Метод для удаления кеша Redis.

        Args:
            cache (str): Кеш-ключ.

        Returns:
            Any: Результат удаления.
        """
        return cls.__instance.redis.delete(cache)

    @classmethod
    async def clear_cache(
        cls,
        logger: LoggerProtocol,
        key_redis: str,
        func: Callable[P, R],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Callable[P, R]:
        """
        Чистка кеша.

        Args:
            logger (LoggerProtocol): Класс для работы с логгером.
            key_redis (str): Ключ для поиска в Redis.
            func (Callable[..., Any]): Оригинальная функция для запуска.

        Returns:
            R: результат функции.
        """
        try:
            if cls.search_key(key_redis) is not None:
                cls.delete_key(key_redis)
                logger.iprint("Кеш удален")
        except redis.ConnectionError as e:
            logger.ierror(f"Не удалось удалить кеш. {e}")

        return await cls.launch_function(func, *args, **kwargs)

    @classmethod
    async def using_cache(
        cls,
        logger: LoggerProtocol,
        key_redis: str,
        func: Callable[P, R],
        time_ttl: int,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Callable[P, R]:
        """
        Использование/сохранение кеша.

        Args:
            logger (LoggerProtocol): Класс для работы с логгером.
            key_redis (str): Ключ для поиска в Redis.
            func (Callable[..., Any]): Оригинальная функция для запуска.
            time_ttl (int): Время жизни кеша. `-1` - бесконечно

        Returns:
            Callable[..., Any]: Кеш/результат функции.
        """
        try:
            if (value_redis := cls.search_key(key_redis)) is None:
                result = await cls.launch_function(func, *args, **kwargs)
                json_value = jsonable_encoder(result)

                cls.save_key(key_redis, json_value, time_ttl)

                logger.iprint("Кеш сохранен")
                return result
            else:
                fixed_json = value_redis.replace("'", '"')
                json_result: R = json.loads(fixed_json)

                logger.iprint("Кеш использован")
                return json_result
        except redis.ConnectionError as e:
            logger.ierror(f"Не удалось использовать кеш. {e}")
            return await cls.launch_function(func, *args, **kwargs)
        except json.decoder.JSONDecodeError:
            logger.ierror(
                f"[Json error] Не удалось использовать кеш. Произошло аварийное удаление ключа."
            )
            cls.delete_key(key_redis)
            return await cls.launch_function(func, *args, **kwargs)

    @staticmethod
    async def launch_function(
        func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
    ) -> Callable[P, Any]:
        if iscoroutinefunction(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)

    @classmethod
    def create_cache_key(cls, name: str, data: Dict[str, Any]) -> str:
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
        return f"icache:{name}:cache:{key_hash}"


class IStatsCache(_RedisService):
    __loger_name = _LogInfo
    __redis_name = _RedisService
    __redis_instance = None
    __log = None

    @classmethod
    def connect_redis_servise(cls):
        if cls.__redis_instance is None:
            cls.__log = cls.__loger_name("stats_cache")
            cls.__redis_instance = cls.__redis_name(cls.__log)

        return cls.__redis_instance

    @classmethod
    def all(cls, *, is_print=False):
        _redis = cls.connect_redis_servise()
        all_keys = _redis.all_keys()

        result: dict[str, str] = {}

        for index, key in enumerate(all_keys, start=1):
            result[index] = {"key": key, "value": _redis.search_key(key)}

        if is_print:
            text_print: list[str] = []
            text_print = [
                f"{index}) {elems['key']} | {elems['value']}"
                for index, elems in result.items()
            ]
            if not text_print:
                text_print.append("Redis пуст")
            cls.__log.iprint("\n".join(text_print))
        return result


@runtime_checkable
class RedisProtocol(Protocol):
    def create_cache_key(): ...


class _CacheCommonMixin:
    @staticmethod
    def creating_dict_arguments(
        func: Callable[..., Any], *args: object, **kwargs: object
    ) -> dict[str, Any]:
        """Метод для парсинга аргументов функции"""
        sig = signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        return dict(bound.arguments)

    @staticmethod
    async def generate_cache_key(
        unique_name: str,
        arguments: dict[str, Any],
        functions: Optional[list[Callable[..., Any]]],
        data: Optional[list[Any]],
        redis: RedisProtocol,
    ) -> str:
        """
        Генерация ключа для кеша.

        Args:
            unique_name (str): Уникальное имя сессии.
            arguments (dict[str, Any]): Все переменные оригинальной функции.
            functions (Optional[list[Callable[..., Any]]]): Все функции переданные в декоратор.
            data (Optional[list[Any]]): Все данные переданные в функцию для кеша.
            redis (RedisProtocol): Класс для работы с редис.

        Raises:
            TypeError: Неверный класс для работы с редис.

        Returns:
            str: Готовый кеш.
        """
        if not isinstance(redis, RedisProtocol):
            raise TypeError(
                f"Класс должен иметь методы: {[name for name, _ in getmembers(RedisProtocol, isfunction) if name != '__subclasshook__']}"
            )

        parameters: dict[str, Any] = {}

        if functions:
            functions = deepcopy(functions)

            if func_result := await _launch_operation(functions, arguments):
                parameters["__ifunc__"] = func_result

        if data:
            data = deepcopy(data)

            if data_result := _substitution_data(data, arguments):
                parameters["__idata__"] = data_result

        key_redis: str = redis.create_cache_key(unique_name, parameters)
        print(f"{parameters} | {key_redis}")
        return key_redis


class IClearCache(_CacheCommonMixin):
    """Декоратор для чистки кеша"""

    __loger_name = _LogInfo
    __redis_name = _RedisService

    def __init__(
        self,
        *,
        unique_name: str,
        functions: Optional[list[Callable[..., Any]]] = None,
        data: Optional[list[Any]] = None,
        time_ttl: int = -1,
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

        if LIMIT_TIME_REDIS > time_ttl >= -1:
            self.time_ttl = time_ttl
        else:
            raise ValueError(
                f"Время должно быть в пределах {LIMIT_TIME_REDIS!r} > time_ttl > -1"
            )

        # устанавливаем сессию логера и редис
        self.log = self.__loger_name(unique_name)
        self.redis = self.__redis_name(self.log)

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """Вызов функции"""

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            all_arguments: dict[str, Any] = self.creating_dict_arguments(
                func, *args, **kwargs
            )

            key_redis = await self.generate_cache_key(
                self.unique_name, all_arguments, self.functions, self.data, self.redis
            )

            return await self.redis.clear_cache(
                self.log, key_redis, func, *args, **kwargs
            )

        return wrapper


class ICache(_CacheCommonMixin):
    """Декоратор для использования кеша"""

    __loger_name = _LogInfo
    __redis_name = _RedisService

    def __init__(
        self,
        *,
        unique_name: str,
        functions: Optional[list[Callable[..., Any]]] = None,
        data: Optional[list[Any]] = None,
        time_ttl: int = -1,
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

        if LIMIT_TIME_REDIS > time_ttl >= -1:
            self.time_ttl = time_ttl
        else:
            raise ValueError(
                f"Время должно быть в пределах {LIMIT_TIME_REDIS!r} > time_ttl > -1"
            )

        # устанавливаем сессию логера и редис
        self.log = self.__loger_name(unique_name)
        self.redis = self.__redis_name(self.log)

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """Вызов функции"""

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            all_arguments: dict[str, Any] = self.creating_dict_arguments(
                func, *args, **kwargs
            )

            key_redis = await self.generate_cache_key(
                self.unique_name, all_arguments, self.functions, self.data, self.redis
            )

            return await self.redis.using_cache(
                self.log, key_redis, func, self.time_ttl, *args, **kwargs
            )

        return wrapper
