import asyncio
import json

from aio_pika import IncomingMessage

from backend.notify_service.app.broker.connection import get_connection
from backend.notify_service.app.handlers import email, telegram
from backend.notify_service.app.utils.parse_body import (
    parse_email_body,
    parse_telegram_body,
)
from backend.notify_service.config import config


async def handle_message(message: IncomingMessage):
    async with message.process():
        body = json.loads(message.body)

        match body["type"]:
            case "email":
                await email.handle(parse_email_body(body["payload"]))
            case "telegram":
                await telegram.handle(parse_telegram_body(body["payload"]))
            case _:
                raise ValueError(f"Ошибка типа: {body['type']} не существует")


async def start_consuming():
    connection = await get_connection()
    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(config.QUEUE_NAME, durable=True)

        await queue.consume(handle_message)

        print("[✔] Консьюмер запущен. Ожидание сообщений...")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_consuming())
