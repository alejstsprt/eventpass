from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi.security import OAuth2PasswordBearer

from ...schemas.user import CreateUser, LoginUser
from ...services.user.get_user_services import get_user_service
from ...services.user.user_services import ManagementUsers
from ...core.logger import Logger
from ...services.user.responses import LOGIN_USER_RESPONSES, CREATE_USER_RESPONSES


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logger = Logger("api_logger")

@router.post(
    '/add_events',
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя ...",
    responses=CREATE_USER_RESPONSES
)
async def create_user(user: CreateUser, service: ManagementUsers = Depends(get_user_service)):
    return {'await service.create_user(user)'}


# Защищённый эндпоинт
@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}