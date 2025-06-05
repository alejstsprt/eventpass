import base64
import hashlib
import hmac
import secrets

from ..core.config import config

SECRET_KEY = config.SECRET_KEY_HMAC


def generate_code_hmac_ticket(user_id: int, event_id: int, ticket_type_id: int) -> str:
    payload = secrets.token_hex(8)  # 16 символов
    data = f"{user_id}:{event_id}:{ticket_type_id}:{payload}"

    signature = hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()[:16]

    return f"TKT.{payload}.{signature}"
