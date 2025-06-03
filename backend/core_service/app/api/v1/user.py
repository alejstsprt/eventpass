from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Response, status
from fastapi_cache.decorator import cache

from ...schemas import (
    CreateUser,
    LoginUser,
    LoginUserResult,
    ManagementUsersProtocol,
    UserRegistrationResult,
)
from ...services import CREATE_USER_RESPONSES, LOGIN_USER_RESPONSES, get_user_service

router = APIRouter()


@router.post(
    "/register",
    summary="Создание аккаунта",
    description="ИНФО: Ручка для создания аккаунта. Принимает в себя name, login, password.",
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_USER_RESPONSES,
)
async def create_user(response: Response, user: CreateUser, service: ManagementUsersProtocol = Depends(get_user_service)):  # type: ignore[no-untyped-def]
    return await service.create_user(response, user)


@router.post(
    "/login",
    summary="Вход в аккаунт",
    description="ИНФО: Ручка для входа в аккаунт. Принимает в себя login, password.",
    status_code=status.HTTP_200_OK,
    responses=LOGIN_USER_RESPONSES,
)
# @cache(expire=80)
async def login_user(response: Response, user: LoginUser, service: ManagementUsersProtocol = Depends(get_user_service)):  # type: ignore[no-untyped-def]
    return await service.login_user(response, user)
