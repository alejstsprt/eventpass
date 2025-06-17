from backend.notify_service.app.tasks.send_email import send_email
from backend.notify_service.app.utils.parse_body import EmailBody


async def handle(payload: EmailBody) -> None:
    await send_email(to=payload.to, title=payload.title, text=payload.text)
