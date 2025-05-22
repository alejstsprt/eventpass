from pydantic import BaseModel

class CreateUser(BaseModel):
    name: str
    login: str
    password: str

class LoginUser(BaseModel):
    login: str
    password: str