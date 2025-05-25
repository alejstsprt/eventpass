from fastapi import APIRouter, Depends, Response
from fastapi_cache.decorator import cache

from ...schemas.user import CreateUser, LoginUser
from ...services.user.get_user_services import get_user_service
from ...services.user.user_services import ManagementUsers
from ...core.logger import Logger
from ...services.user.responses import LOGIN_USER_RESPONSES, CREATE_USER_RESPONSES


router = APIRouter()

logger = Logger("api_logger")

@router.post(
    '/create-user',
    summary="Создание аккаунта",
    description="ИНФО: Ручка для создания аккаунта. Принимает в себя имя, логин и пароль.",
    responses=CREATE_USER_RESPONSES
)
async def create_user(response: Response, user: CreateUser, service: ManagementUsers = Depends(get_user_service)):
    return await service.create_user(response, user)

@router.post(
    '/login-user',
    summary="Вход в аккаунт",
    description="ИНФО: Ручка для входа в аккаунт. Принимает в себя логин и пароль.",
    responses=LOGIN_USER_RESPONSES
)
@cache(expire=80)
async def login_user(response: Response, user: LoginUser, service: ManagementUsers = Depends(get_user_service)):
    return await service.login_user(response, user)