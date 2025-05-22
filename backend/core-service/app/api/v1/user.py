from fastapi import APIRouter, Depends

from ...schemas.user import CreateUser, LoginUser
from ...services.user.get_user_services import get_user_service
from ...services.user.user_services import ManagementUsers
from ...core.logger import Logger
from fastapi_cache.decorator import cache


router = APIRouter()

logger = Logger("api_logger")

@router.post(
    '/create_user',
    summary="Создание аккаунта",
    description="ИНФО: Ручка для создания аккаунта. Принимает в себя имя, логин и пароль.",
    responses={
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
)
async def create_user(user: CreateUser, service: ManagementUsers = Depends(get_user_service)):
    return await service.create_user(user)

@router.post(
    '/login_user',
    summary="Вход в аккаунт",
    description="ИНФО: Ручка для входа в аккаунт. Принимает в себя логин и пароль.",
    responses={
        200: {
            "description": "Успешный ответ: Пользователь вошел",
            "content": {
                "application/json": {
                    "example": {"result": True, "id": 6, "name": "qwe"}
                }
            }
        },
        400: {
            "description": "Ошибки с кодом 400",
            "content": {
                "application/json": {
                    "examples": {
                        "login_exists": {
                            "summary": "Неверный логин",
                            "value": {'result': False, 'error': 'Неверный логин'}
                        },
                        "registration_failed": {
                            "summary": "Неверный пароль",
                            "value": {'result': False, 'error': 'Неверный пароль'}
                        }
                    }
                }
            }
        }
    }
)
@cache(expire=60)
async def login_user(user: LoginUser, service: ManagementUsers = Depends(get_user_service)):
    return await service.login_user(user)