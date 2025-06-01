from datetime import datetime
from typing import Literal, NotRequired, Optional, TypedDict

from sqlalchemy import Column


# [SearchUserResult]
class SearchUserResult(TypedDict):
    """Формат ответа"""

    id: Optional[int]
    login: Optional[str]


# [UserRegistrationResult]
class UserRegistrationResult(TypedDict):
    """Формат ответа"""

    result: Literal[True]
    user_id: NotRequired[Column[int]]
    error: NotRequired[str]


# [EventCreatedResult]
class EventDetails(TypedDict):
    """-> EventCreatedResult"""

    id: Column[int]
    status: Column[str]
    creator_id: Column[int]
    title: Column[str]
    description: Column[str]
    address: Column[str]
    time_create: Column[datetime]


class EventCreatedResult(TypedDict):
    """Формат ответа"""

    result: Literal[True]
    event: EventDetails


# [LoginUserResult]
class LoginUserResult(TypedDict):
    """Формат ответа"""

    id: Column[int]
    name: Column[str]
