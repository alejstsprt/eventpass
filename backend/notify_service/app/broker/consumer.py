import json

from aio_pika import IncomingMessage
from app.broker.connection import get_connection
from app.handlers import email, telegram
from app.utils.parse_payload import parse_payload


async def handle_message(message: IncomingMessage):
    async with message.process():
        payload = json.loads(message.body)
        data = parse_payload(payload)

        match data.type:
            case "email":
                await email.handle(data)
            case "telegram":
                await telegram.handle(data)
            case _:
                raise ValueError(f"Ошибка типа: {data.type} не существует")


async def start_consuming():
    connection = await get_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue("notifications", durable=True)

    await queue.consume(handle_message)
