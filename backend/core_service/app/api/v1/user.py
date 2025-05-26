from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Response
from fastapi_cache.decorator import cache

from ...services import get_user_service, LOGIN_USER_RESPONSES, CREATE_USER_RESPONSES
from ...core.logger import Logger

if TYPE_CHECKING:
    from ...schemas import CreateUser, LoginUser, UserRegistrationResult, LoginUserResult
    from ...services import ManagementUsers


router = APIRouter()

logger = Logger("api_logger")

@router.post(
    '/create-user',
    summary="Создание аккаунта",
    description="ИНФО: Ручка для создания аккаунта. Принимает в себя имя, логин и пароль.",
    responses=CREATE_USER_RESPONSES
)
async def create_user(response: Response, user: 'CreateUser', service: 'ManagementUsers' = Depends(get_user_service)) -> 'UserRegistrationResult':
    return await service.create_user(response, user)

@router.post(
    '/login-user',
    summary="Вход в аккаунт",
    description="ИНФО: Ручка для входа в аккаунт. Принимает в себя логин и пароль.",
    responses=LOGIN_USER_RESPONSES
)
@cache(expire=80)
async def login_user(response: Response, user: 'LoginUser', service: 'ManagementUsers' = Depends(get_user_service)) -> 'LoginUserResult':
    return await service.login_user(response, user)