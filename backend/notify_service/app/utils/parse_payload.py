from pydantic import BaseModel


class Payload(BaseModel):
    type: str
    to: str
    message: str
    subject: str | None = None  # только для email


def parse_payload(raw: dict) -> Payload:
    return Payload(**raw)
