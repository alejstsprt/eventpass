from fastapi import APIRouter, Cookie, Depends, Request, Response, status

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
from services import CREATE_USER_RESPONSES, LOGIN_USER_RESPONSES, get_user_service

router = APIRouter()


@router.get(
    "",
    summary="Информация о пользователе",
    description="ИНФО: Ручка возвращает информацию о пользователе. ID user берется из токена.",
    status_code=status.HTTP_200_OK,
    responses=None,  # TODO: сделать
)
async def create_user(
    jwt_token: str = Cookie(None),
    service: ManagementUsersProtocol = Depends(get_user_service),
) -> GetUserInfoResponseDTO:
    return await service.get_info_user(jwt_token)


@router.post(
    "/register",
    summary="Создание аккаунта",
    description="ИНФО: Ручка для создания аккаунта. Принимает в себя name, login, password.",
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_USER_RESPONSES,
)
async def create_user(
    response: Response,
    user: CreateUserDTO,
    rabbit_producer: RabbitProducer = Depends(get_rabbit_producer),
    service: ManagementUsersProtocol = Depends(get_user_service),
) -> CreateUserResponseDTO:
    return await service.create_user(response, user, rabbit_producer)


@router.post(
    "/login",
    summary="Вход в аккаунт",
    description="ИНФО: Ручка для входа в аккаунт. Принимает в себя login, password.",
    status_code=status.HTTP_200_OK,
    responses=LOGIN_USER_RESPONSES,
)
async def login_user(
    response: Response,
    user: LoginUserDTO,
    service: ManagementUsersProtocol = Depends(get_user_service),
) -> LoginUserResponseDTO:
    return await service.login_user(response, user)
