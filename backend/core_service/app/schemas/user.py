from pydantic import BaseModel, EmailStr, Field


CorrectForm = Field(min_length=2, max_length=50)

class LoginUser(BaseModel):
    login: EmailStr
    password: str = CorrectForm

class CreateUser(LoginUser):
    name: str = CorrectForm