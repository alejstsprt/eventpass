from asyncio import Lock
import json

from aio_pika import DeliveryMode, Message, connect_robust
from aio_pika.exceptions import AMQPConnectionError


class RabbitProducer:
    """RabbitMQ продюсер"""

    def __init__(self, *args, **kwargs):
        self.__args_to_connect = args
        self.__kwargs_to_connect = kwargs
        self.__connect_rabbit = None
        self.__channel_rabbit = None
        self.__lock = Lock()

    async def connect(self) -> None:
        """Открыть соединение с Rabbit"""
        async with self.__lock:
            try:
                self.__connect_rabbit = await connect_robust(
                    *self.__args_to_connect,
                    **self.__kwargs_to_connect,
                )
                self.__channel_rabbit = await self.__connect_rabbit.channel()
            except AMQPConnectionError:
                raise ConnectionError(
                    "Произошла ошибка соединения с RabbitMQ. Наверное, сервер не включен."
                ) from None

    async def close(self) -> None:
        """Закрыть соединение с Rabbit"""
        await self.__connect_rabbit.close()

    async def add_to_queue(
        self,
        queue_name: str,
        body: object,
        durable=True,
        delivery_mode=DeliveryMode.PERSISTENT,
    ) -> None:
        """Добавление в очередь Rabbit"""
        if self.__connect_rabbit is None or self.__channel_rabbit is None:
            raise ConnectionError(
                "Ошибка. Подключитесь к RabbitMQ через метод connect()"
            ) from None

        if self.__connect_rabbit.is_closed or self.__channel_rabbit.is_closed:
            await self.connect()

        await self.__channel_rabbit.declare_queue(queue_name, durable=durable)

        if isinstance(body, str):
            message_body = body.encode()
        elif isinstance(body, dict):
            message_body = json.dumps(body).encode()
        elif isinstance(body, bytes):
            message_body = body
        else:
            raise ValueError("Тип данных не определен")

        message = Message(message_body, delivery_mode=delivery_mode)

        await self.__channel_rabbit.default_exchange.publish(
            message, routing_key=queue_name
        )
