from pydantic import BaseModel

class loginUser(BaseModel):
    login: str
    password: str