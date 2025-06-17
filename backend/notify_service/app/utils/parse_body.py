from pydantic import BaseModel


class EmailBody(BaseModel):
    to: str
    title: str
    text: str


class TelegramBody(BaseModel):
    user_id: int
    test: str


def parse_email_body(body: dict) -> EmailBody:
    return EmailBody(**body)


def parse_telegram_body(body: dict) -> TelegramBody:
    return TelegramBody(**body)
