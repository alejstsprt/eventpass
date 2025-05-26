from typing import TypedDict, Literal, NotRequired, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
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
    user_id: NotRequired['Column'[int]]
    error: NotRequired[str]

# [EventCreatedResult]
class EventDetails(TypedDict):
    id: 'Column'[int]
    creator_id: 'Column'[int]
    title: 'Column'[str]
    description: 'Column'[str]
    address: 'Column'[str]
    time_create: 'Column'[datetime]

class EventCreatedResult(TypedDict):
    """Формат ответа"""
    result: Literal[True]
    event: EventDetails

# [LoginUserResult]
class LoginUserResult(TypedDict):
    """Формат ответа"""
    id: 'Column'[int]
    name: 'Column'[str]