from typing import TypedDict, Literal, NotRequired, Optional
from datetime import datetime

from sqlalchemy import Column


class SearchUserResult(TypedDict):
    id: Optional[int]
    login: Optional[str]

class UserRegistrationResult(TypedDict):
    result: Literal[True]
    user_id: NotRequired[Column[int]]
    error: NotRequired[str]

class EventDetails(TypedDict):
    id: Column[int]
    creator_id: Column[int]
    title: Column[str]
    description: Column[str]
    address: Column[str]
    time_create: Column[datetime]

class EventCreatedResult(TypedDict):
    result: Literal[True]
    event: EventDetails