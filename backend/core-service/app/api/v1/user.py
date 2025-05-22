from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from ...schemas.user import loginUser
from ...models.session import get_db
from ...services.user.get_user_services import get_create_user_services
from ...services.user.user_services import CreateUser


router = APIRouter()


@router.post('/create_user', summary="Создание аккаунта", description="ИНФО: Ручка для создания аккаунта. Принимает в себя логин и пароль.")
async def create_user(user: loginUser, service: CreateUser = Depends(get_create_user_services)):
    return service.create_user(user)