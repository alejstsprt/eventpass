from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from backend.core_service.app.core.config import config
from backend.core_service.app.core.logger import logger_api
from backend.core_service.app.infrastructure.messaging.producer import RabbitProducer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    producer = RabbitProducer(login=config.RABBIT_USER, password=config.RABBIT_PASSWORD)
    app.state.rabbit_producer = producer
    await producer.connect()
    logger_api.info("Продюсер Rabbit запущен")
    yield
    await producer.close()
    logger_api.info("Продюсер Rabbit завершил свою работу")
