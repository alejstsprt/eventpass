from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


# [LoginUser]
class LoginUser(BaseModel):
    login: Annotated[EmailStr, Field(
        description="Логин пользователя",
        min_length=2,
        max_length=50
    )]

    password: Annotated[str, Field(
        description="Пароль пользователя",
        examples=["mypassword123"],
        min_length=5,
        max_length=50
    )]

# [CreateUser]
class CreateUser(LoginUser):
    name: Annotated[str, Field(
        description="Имя пользователя",
        examples=["Витя"],
        min_length=5,
        max_length=50
    )]