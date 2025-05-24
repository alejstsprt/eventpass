from typing import Optional

from fastapi import APIRouter, Depends, Cookie
from fastapi_cache.decorator import cache

from ...schemas.user_tickets import *
from ...services.user_tickets.get_user_services import get_user_service
from ...services.user_tickets.user_tickets_services import ManagementEvents
from ...core.logger import Logger
from ...services.user_tickets.responses import LOGIN_USER_RESPONSES, CREATE_USER_RESPONSES


router = APIRouter()

logger = Logger("api_logger")

@router.post(
    '/add_events',
    summary="Создание мероприятия",
    description="ИНФО: Ручка для создания мероприятия. Принимает в себя ...",
    responses=CREATE_USER_RESPONSES
)
async def create_user(
        user: CreateUser,
        service: ManagementEvents = Depends(get_user_service),
        jwt_token: Optional[str] = Cookie(None)
    ):
    return {jwt_token}