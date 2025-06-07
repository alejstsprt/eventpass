import base64
import hashlib
import hmac
import secrets

from core.config import config


def generate_code_hmac_ticket(user_id: int, event_id: int, ticket_type_id: int) -> str:
    payload = secrets.token_hex(8)  # 16 символов
    data = f"{user_id}:{event_id}:{ticket_type_id}:{payload}"

    signature = hmac.new(
        config.SECRET_KEY_HMAC, data.encode(), hashlib.sha256
    ).hexdigest()[:16]

    return f"TKT.{payload}.{signature}"
