from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from backend.core_service.app.core.logger import logger_api


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any, None]:
    logger_api.info("Приложение запущено")
    yield
    logger_api.info("Приложение завершило свою работу")
