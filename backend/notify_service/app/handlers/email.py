from app.tasks.send_email import send_email
from app.utils.parse_payload import Payload


async def handle(payload: Payload) -> None:
    await send_email(to=payload.to, subject=payload.subject, message=payload.message)
