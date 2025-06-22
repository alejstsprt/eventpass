from typing import Annotated

from app.core.config import config
from app.schemas.pydantic.routers.users import AddUserInReminderDTO, EditUserDTO
from fastapi import APIRouter, Body, Depends, Path, status

router = APIRouter()

# Табл 1: user_id | email | name | event_id | text | start_at
# Табл 2: event_id | title | address


@router.post(
    "",
    summary="Ручка для создания напоминаний",
    description="",
    status_code=status.HTTP_201_CREATED,
)
async def add_reminder(
    data_users: Annotated[
        AddUserInReminderDTO,
        Body(..., description="Данные пользователей для создания напоминания"),
    ],
):
    return data_users


@router.patch(
    "/{user_id}",
    summary="Ручка для редактирования напоминания",
    description="",
    status_code=status.HTTP_200_OK,
)
async def edit_reminder(
    user_id: Annotated[
        int, Path(..., description="ID пользователя", ge=1, le=config.MAX_ID)
    ],
    data_users: Annotated[
        EditUserDTO, Body(..., description="Новые данные мероприятия")
    ],
):
    return {user_id: data_users}


@router.delete(
    "/{user_id}",
    summary="Ручка для удаления напоминания",
    description="",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_reminder(
    user_id: Annotated[
        int, Path(..., description="ID пользователя", ge=1, le=config.MAX_ID)
    ],
):
    return user_id
