from typing import Annotated

from app.core.config import config
from app.schemas.pydantic.routers.events import AddEventsDTO, EditEventDTO
from fastapi import APIRouter, Body, Depends, Path, status

router = APIRouter()


@router.post(
    "",
    summary="Ручка для добавление мероприятий",
    description="ВНИМАНИЕ: ID мероприятия должен быть равен тому ID, который был указал в ручке /user",
    status_code=status.HTTP_201_CREATED,
)
def add_events(
    data_events: Annotated[
        AddEventsDTO, Body(..., description="Данные мероприятий для добавления")
    ],
):
    return data_events


@router.patch(
    "/{event_id}",
    summary="Ручка для редактирования мероприятия",
    description="ВНИМАНИЕ: ID мероприятия должен быть равен тому ID, который был указал в ручке /user",
    status_code=status.HTTP_201_CREATED,
)
def edit_event(
    event_id: Annotated[
        int, Path(..., description="ID мероприятия", ge=1, le=config.MAX_ID)
    ],
    data_events: Annotated[
        EditEventDTO, Body(..., description="Данные мероприятия для редактирования")
    ],
):
    return {event_id: data_events}


@router.delete(
    "/{event_id}",
    summary="Ручка для удаления мероприятия",
    description="ВНИМАНИЕ: ID мероприятия должен быть равен тому ID, который был указал в ручке /user",
    status_code=status.HTTP_201_CREATED,
)
def delete_event(
    event_id: Annotated[
        int, Path(..., description="ID мероприятия", ge=1, le=config.MAX_ID)
    ],
):
    return
