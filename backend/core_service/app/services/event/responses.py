from typing import Any

CREATE_EVENT_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {
        "description": "Успешный ответ: Пользователь вошел",
        "content": {
            "application/json": {
                "example": {
                    "result": True,
                    "event": {
                        "id": "id",
                        "status": "status",
                        "creator_id": "creator_id",
                        "title": "title",
                        "description": "description",
                        "address": "address",
                        "time_create": "datetime",
                    },
                }
            }
        },
    },
    401: {
        "description": "Ошибки пользователя",
        "content": {
            "application/json": {
                "examples": {
                    "server_error": {
                        "summary": "Внутренняя ошибка сервера",
                        "value": {"detail": "Внутренняя ошибка сервера"},
                    },
                    "validation_error": {
                        "summary": "Неверные данные",
                        "value": {"detail": "Неверные данные"},
                    },
                    "no_token_error": {
                        "summary": "Токен отсутствует",
                        "value": {"detail": "Токен отсутствует"},
                    },
                    "token_error": {
                        "summary": "Неверный токен",
                        "value": {"detail": "Неверный токен"},
                    },
                }
            }
        },
    },
}
