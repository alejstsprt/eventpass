import aio_pika
from config import settings


async def get_connection():
    return await aio_pika.connect_robust(settings.rabbitmq_url)
