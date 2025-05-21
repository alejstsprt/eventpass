from fastapi import APIRouter, Request, Depends

from sqlalchemy.orm import Session

from ...schemas.user import loginUser

from ...models.session import get_db
from ...models.crud import is_exists_login

from ...exceptions import s

# from ...security.hashing import is_


router = APIRouter()


@router.post('/create_user', summary="Создание аккаунта", description="ИНФО: Ручка для создания аккаунта. Принимает в себя логин и пароль.")
async def test(request: loginUser, db: Session = Depends(get_db)):
    is_user = await is_exists_login(request.login)
    if not is_user['result']:
        raise

    return {'yes': request.password}