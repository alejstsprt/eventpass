from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from schemas.pydantics.cfg_base_model import ConfigBaseModelResponseDTO


# [LoginUser]
class LoginUserDTO(BaseModel):
    login: Annotated[
        EmailStr, Field(description="Логин пользователя", min_length=2, max_length=100)
    ]

    password: Annotated[
        str,
        Field(
            description="Пароль пользователя",
            examples=["mypassword123"],
            min_length=5,
            max_length=100,
        ),
    ]


class LoginUserResponseDTO(ConfigBaseModelResponseDTO):
    id: int
    name: str


# [CreateUser]
class CreateUserDTO(LoginUserDTO):
    name: Annotated[
        str,
        Field(
            description="Имя пользователя",
            examples=["Витя"],
            min_length=2,
            max_length=100,
        ),
    ]


class CreateUserResponseDTO(ConfigBaseModelResponseDTO):
    id: int


# [GetUserInfo]
class GetUserInfoResponseDTO(ConfigBaseModelResponseDTO):
    id: int
    name: str
    login: str
