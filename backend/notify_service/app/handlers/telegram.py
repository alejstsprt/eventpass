from backend.notify_service.app.tasks.send_telegram import send_telegram
from backend.notify_service.app.utils.parse_body import TelegramBody


async def handle(payload: TelegramBody) -> None:
    await send_telegram(user_id=payload.user_id, text=payload.text)
