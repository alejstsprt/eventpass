from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from ...schemas.user import loginUser
from ...models.session import get_db
from ...models.crud import is_exists_login, user_registration
from ...exceptions import LoginAlreadyExistsException, RegistrationFailedException
from ...security.hashing import hash_password


class CreateUser:
    def __init__(self, db):
        self.db = db

    def create_user(self, login, password):
        return {'result': True}