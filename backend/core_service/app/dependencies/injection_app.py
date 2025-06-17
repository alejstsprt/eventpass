from fastapi import Request

from infrastructure.messaging.producer import RabbitProducer


def get_rabbit_producer(request: Request) -> RabbitProducer:
    return request.app.state.rabbit_producer
