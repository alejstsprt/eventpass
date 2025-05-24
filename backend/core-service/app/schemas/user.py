from pydantic import BaseModel, EmailStr, Field


CorrectForm = Field(min_length=2, max_length=50)

class CreateUser(BaseModel):
    name: str = CorrectForm
    login: EmailStr
    password: str = CorrectForm

class LoginUser(BaseModel):
    login: EmailStr
    password: str = CorrectForm