from typing import Any


LOGIN_USER_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {
        "description": "Успешный ответ: Пользователь вошел",
        "content": {"application/json": {"example": {"id": 1, "name": "alexey"}}}
    },
    401: {
        "description": "Ошибки пользователя",
        "content": {
            "application/json": {
                "examples": {
                    "login_exists": {"summary": "Неверный логин", "value": {'detail': 'Неверный логин'}},
                    "registration_failed": {"summary": "Неверный пароль", "value": {'detail': 'Неверный пароль'}}
                }
            }
        }
    }
}

CREATE_USER_RESPONSES: dict[int | str, dict[str, Any]] = {
    200: {
        "description": "Успешный ответ: Пользователь зарегестрирован",
        "content": {
            "application/json": {
                "example": {'result': True}
            }
        }
    },
    400: {
        "description": "Ошибки с кодом 400",
        "content": {
            "application/json": {
                "examples": {
                    "login_exists": {
                        "summary": "Логин занят",
                        "value": {"detail": "Логин уже занят"}
                    },
                    "registration_failed": {
                        "summary": "Ошибка регистрации",
                        "value": {"detail": "Ошибка при регистрации"}
                    }
                }
            }
        }
    }
}