from datetime import datetime

from pydantic import BaseModel, Field


# [CreateEvent]
class CreateEvent(BaseModel):
    title: str = Field(min_length=2, max_length=20) # название мероприятия
    description: str = Field(min_length=2, max_length=1000) # описание мероприятия
    address: str = Field(min_length=2, max_length=50) # адрес мероприятия