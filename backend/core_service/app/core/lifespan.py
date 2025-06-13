from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core_service.app.core.logger import logger_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger_api.info("Приложение запущено")
    yield
    logger_api.info("Приложение завершило свою работу")
