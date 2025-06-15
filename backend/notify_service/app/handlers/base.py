from abc import ABC, abstractmethod

from app.utils.parse_payload import Payload


class BaseHandler(ABC):
    @abstractmethod
    async def handle(self, payload: Payload) -> None: ...
