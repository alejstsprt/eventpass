from fastapi import APIRouter, Request, Depends

from sqlalchemy.orm import Session

from ...schemas.user import loginUser

from ...models.session import get_db
from ...models.crud import is_exists_login, user_registration

from ...exceptions import LoginAlreadyExistsException, RegistrationFailedException

from ...security.hashing import hash_password


router = APIRouter()


@router.post('/create_user', summary="Создание аккаунта", description="ИНФО: Ручка для создания аккаунта. Принимает в себя логин и пароль.")
async def test(request: loginUser, db: Session = Depends(get_db)):
    is_user = await is_exists_login(db, request.login)
    if is_user['result']:
        raise LoginAlreadyExistsException()

    hash_pass = hash_password(request.login)
    result = await user_registration(db, request.login, hash_pass)
    if result['result']:
        return {'result': True}
    else:
        raise RegistrationFailedException()