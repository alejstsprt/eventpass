import aio_pika

from backend.notify_service.config import config


async def get_connection():
    return await aio_pika.connect_robust(
        login=config.RABBIT_USER,
        password=config.RABBIT_PASSWORD,
    )
