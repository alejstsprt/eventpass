from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

from backend.core_service.app.core.config import config
from backend.core_service.app.core.logger import logger_api
from backend.core_service.app.infrastructure.messaging.producer import RabbitProducer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    producer = RabbitProducer(login=config.RABBIT_USER, password=config.RABBIT_PASSWORD)
    app.state.rabbit_producer = producer
    await producer.connect()
    logger_api.info("Продюсер Rabbit запущен")

    redis_client = redis.from_url(
        "redis://localhost:6379", encoding="utf-8", decode_responses=True
    )
    await FastAPILimiter.init(redis_client)
    logger_api.info("Redis для FastAPILimiter подключен")

    yield

    await producer.close()
    logger_api.info("Продюсер Rabbit завершил свою работу")
