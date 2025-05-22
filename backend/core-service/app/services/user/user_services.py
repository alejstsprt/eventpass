from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from ...schemas.user import loginUser
from ...models.session import get_db
from ...models.crud import is_exists_login, user_registration
from ...core.exceptions import LoginAlreadyExistsException, RegistrationFailedException
from ...security.hashing import hash_password


class CreateUser:
    def __init__(self, db):
        self.db = db

    async def create_user(self, user):
        is_user = await is_exists_login(self.db, user.login)
        if is_user['result']:
            raise LoginAlreadyExistsException()

        hash_pass = hash_password(user.password)
        result = await user_registration(self.db, user.login, hash_pass)
        if result['result']:
            return {'result': True}
        else:
            raise RegistrationFailedException()