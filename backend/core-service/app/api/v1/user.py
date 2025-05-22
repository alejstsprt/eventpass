from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from ...schemas.user import loginUser
from ...models.session import get_db
from ...services.user.get_user_services import get_user_service
from ...services.user.user_services import CreateUser
from ...core.logger import Logger
# from fastapi_cache.decorator import cache


router = APIRouter()

logger = Logger("api_logger")

@router.post(
    '/create_user',
    summary="Создание аккаунта",
    description="ИНФО: Ручка для создания аккаунта. Принимает в себя логин и пароль."
)
async def create_user(user: loginUser, service: CreateUser = Depends(get_user_service)):
    logger.warning('Срочно')
    return await service.create_user(user)