import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from backend.core_service.app.infrastructure.cache_v2 import (
    ICache,
    ICacheWriter,
    IParam,
    IStatsCache,
)

# IStatsCache.all(is_print=True)


def test_func(*args, **kwargs):
    print("Была вызвана доп функция. входные:", args, kwargs)
    return args


@ICache(
    unique_name="test-2",
    functions=[
        IParam(test_func),
        IParam(test_func),
        IParam(test_func),
        IParam(test_func),
        IParam(test_func),
        IParam(test_func),
        IParam(test_func),
        IParam(test_func),
        IParam(test_func),
        IParam(
            test_func,
            "Этап 1",
            IParam(
                test_func,
                "Этап 2",
                IParam(
                    test_func,
                    "Этап 3",
                    IParam(
                        test_func,
                        "Этап 4",
                    ),
                ),
            ),
        ),
    ],
)
def test_cahce(id: int = 10, ff=20):
    print("Функция 1 вызвана", id)
    return id


@ICache(unique_name="test-2", functions=[ICacheWriter(test_func)])
async def test_cahce2(id):
    print("Функция 2 вызвана", id)
    return id


@ICache(unique_name="test-3", functions=[ICacheWriter(IParam(test_func, "id"))])
async def test_cahce3(id=10, dd=2):
    print("Функция 3 вызвана", id)
    return id


while True:
    if (mm := input()) == "1":
        asyncio.run(test_cahce(input()))
    elif mm == "2":
        asyncio.run(test_cahce2(input()))
    else:
        asyncio.run(test_cahce3(input()))
