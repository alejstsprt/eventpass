from typing import Annotated

from fastapi import APIRouter, Body, Cookie, Depends, Response, status
from fastapi_limiter.depends import RateLimiter

from dependencies.injection_app import get_rabbit_producer
from infrastructure.messaging.producer import RabbitProducer
from schemas import (
    CreateUserDTO,
    CreateUserResponseDTO,
    GetUserInfoResponseDTO,
    LoginUserDTO,
    LoginUserResponseDTO,
    ManagementUsersProtocol,
)
from services import get_user_service

router = APIRouter()


@router.get(
    "",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Информация о пользователе",
    description="ИНФО: Ручка возвращает информацию о пользователе. ID user берется из токена.",
    status_code=status.HTTP_200_OK,
)
async def get_user(
    jwt_token: Annotated[
        str, Cookie(..., description="JWT токен пользователя", max_length=1_000)
    ],
    service: Annotated[ManagementUsersProtocol, Depends(get_user_service)],
) -> GetUserInfoResponseDTO:
    return await service.get_info_user(jwt_token)


@router.post(
    "/register",
    dependencies=[Depends(RateLimiter(times=8, seconds=60))],
    summary="Создание аккаунта",
    description="ИНФО: Ручка для создания аккаунта. Принимает в себя name, login, password.",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    response: Response,
    user: Annotated[
        CreateUserDTO, Body(..., description="Данные пользователя для регистрации")
    ],
    service: Annotated[ManagementUsersProtocol, Depends(get_user_service)],
    rabbit_producer: Annotated[RabbitProducer, Depends(get_rabbit_producer)],
) -> CreateUserResponseDTO:
    return await service.create_user(response, user, rabbit_producer)


@router.post(
    "/login",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
    summary="Вход в аккаунт",
    description="ИНФО: Ручка для входа в аккаунт. Принимает в себя login, password.",
    status_code=status.HTTP_200_OK,
)
async def login_user(
    response: Response,
    user: Annotated[LoginUserDTO, Body(..., description="Данные для входа")],
    service: Annotated[ManagementUsersProtocol, Depends(get_user_service)],
) -> LoginUserResponseDTO:
    return await service.login_user(response, user)
