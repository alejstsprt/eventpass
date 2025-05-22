from fastapi import APIRouter, Depends

from ...schemas.user import LoginUser
from ...services.user.get_user_services import get_user_service
from ...services.user.user_services import ManagementUsers
from ...core.logger import Logger
# from fastapi_cache.decorator import cache


router = APIRouter()

logger = Logger("api_logger")

@router.post(
    '/create_user',
    summary="Создание аккаунта",
    description="ИНФО: Ручка для создания аккаунта. Принимает в себя логин и пароль.",
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
            "description": "Возможные ошибки:",
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
async def create_user(user: LoginUser, service: ManagementUsers = Depends(get_user_service)):
    return await service.create_user(user)