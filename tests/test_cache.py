import asyncio
import sys
from pathlib import Path

import pytest

# from aiocache import caches

sys.path.append(str(Path(__file__).parent.parent))


from backend.core_service.app.infrastructure.cache_v2 import (
    ICache,
    ICacheWriter,
    IClearCache,
    IParam,
    istats,
)

# istats.all_cache(is_print=True)


# ========== MOCK DATA ==========

# Список для отслеживания всех вызовов функций
calls = []


# Пример функции, которую можно использовать в IParam
def mock_func(*args, **kwargs):
    calls.append(("mock_func", args, kwargs))  # логируем вызов
    return f"key-{args}-{kwargs}"  # возвращаем фиктивный ключ


# Пример функции, возвращающей значение для кеш-ключа
def writer_func():
    calls.append(("writer_func",))  # логируем вызов
    return "writer"  # фиктивное значение, которое попадет в ключ кеша


# ========== ТЕСТ СИНХРОННОЙ ФУНКЦИИ ==========


@ICache(unique_name="test_sync", functions=[IParam(mock_func, 1, test=True)])
def sync_func(x=5):
    calls.append(("sync_func", x))  # логируем вызов основной функции
    return x * 2


def test_sync_cache_basic():
    calls.clear()  # очищаем историю вызовов

    result1 = sync_func(10)  # первый вызов - должен исполниться и закешироваться
    result2 = sync_func(10)  # второй вызов - должен использовать кеш

    # Проверка: результат функции корректен
    assert result1 == 20
    assert result2 == 20

    # Проверка: sync_func была вызвана только 1 раз, т.к. кеш сработал
    assert calls.count(("sync_func", 10)) <= 1

    # Проверка: mock_func (из IParam) точно была вызвана
    assert any(call[0] == "mock_func" for call in calls)


test_sync_cache_basic()


# ========== ТЕСТ АСИНХРОННОЙ ФУНКЦИИ ==========


@ICache(unique_name="test_async", functions=[ICacheWriter(writer_func)])
async def async_func(x):
    calls.append(("async_func", x))  # логируем вызов основной async-функции
    return x + 1


@pytest.mark.asyncio
async def test_async_cache_basic():
    calls.clear()

    result1 = await async_func(3)  # первый вызов - исполнится и кешируется
    result2 = await async_func(3)  # второй вызов - должен взять из кеша

    # Проверка: функция возвращает корректный результат
    assert result1 == 4
    assert result2 == 4

    # Проверка: async_func была вызвана только один раз
    assert calls.count(("async_func", 3)) == 1

    # Проверка: writer_func была вызвана — значит ключ кеша формировался с её участием
    assert ("writer_func",) in calls


# ========== ТЕСТ ОЧИСТКИ КЕША ==========


@ICache(unique_name="test_clear", tags=["clear_tag"])
async def clearable_func(x):
    calls.append(("clearable_func", x))  # логируем вызов основной функции
    return x * 10


@IClearCache(unique_name="clear", tags_delete=["clear_tag"])
async def clear_cache():
    calls.append(("clear_cache",))  # логируем факт вызова очистки кеша
    return True


@pytest.mark.asyncio
async def test_cache_clear():
    calls.clear()

    await clearable_func(2)  # Первый вызов — должен исполниться и закешироваться
    await clearable_func(2)  # Второй вызов — должен взять из кеша

    await clear_cache()  # Вызываем очистку кеша по тегу

    await clearable_func(2)  # После очистки кеша функция должна вызваться снова

    # Проверка: clearable_func была вызвана 2 раза (до и после очистки кеша)
    assert calls.count(("clearable_func", 2)) == 2

    # Проверка: clear_cache действительно была вызвана
    assert ("clear_cache",) in calls


# import asyncio
# import sys
# from pathlib import Path

# sys.path.append(str(Path(__file__).parent.parent))

# from backend.core_service.app.infrastructure.cache_v2 import (
#     ICache,
#     IClearCache,
#     ICacheWriter,
#     IParam,
#     IStatsCache,
# )

# # IStatsCache.all(is_print=True)


# def test_func(*args, **kwargs):
#     print("Была вызвана доп функция. входные:", args, kwargs)
#     return args


# @ICache(
#     unique_name="test-2",
#     functions=[
#         IParam(test_func),
#         IParam(test_func),
#         IParam(test_func),
#         IParam(test_func),
#         IParam(test_func),
#         IParam(test_func),
#         IParam(test_func),
#         IParam(test_func),
#         IParam(test_func)
#     ]
# )
# def test_cahce(id: int = 10, ff=20):
#     print("Функция 1 вызвана", id)
#     return id


# @ICache(unique_name="test-2", functions=[ICacheWriter(test_func)])
# async def test_cahce2(id):
#     print("Функция 2 вызвана", id)
#     return id


# @ICache(unique_name="test-3", functions=[ICacheWriter(IParam(test_func, "id"))])
# async def test_cahce3(id=10, dd=2):
#     print("Функция 3 вызвана", id)
#     return id

# @ICache(unique_name="test", tags=["mylite"])
# async def test_cahce5(id=10, dd=2):
#     print("Функция 5 вызвана", id)
#     return id
# @IClearCache(unique_name="123", tags_delete=["mylite"])
# async def test_cahce6(id=10):
#     print("Функция 6 вызвана", id)
#     return id


# while True:
#     if (mm := input()) == "1":
#         asyncio.run(test_cahce(input()))
#     elif mm == "2":
#         asyncio.run(test_cahce2(input()))
#     elif mm == "3":
#         asyncio.run(test_cahce5(input()))
#     elif mm == "4":
#         asyncio.run(test_cahce6(input()))
#     else:
#         asyncio.run(test_cahce3(input()))
