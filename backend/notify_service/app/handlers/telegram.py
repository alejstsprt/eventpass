from app.tasks.send_telegram import send_telegram
from app.utils.parse_payload import Payload


async def handle(payload: Payload) -> None:
    await send_telegram(to=payload.to, message=payload.message)
