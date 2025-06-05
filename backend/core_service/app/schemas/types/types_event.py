from typing import NewType

# [Event]
IntEventCreatorId = NewType("IntEventCreatorId", int)
"""ID создателя мероприятия (Integer)"""

StrEventTitle = NewType("StrEventTitle", str)
"""Название мероприятия (String)"""

StrEventDescription = NewType("StrEventDescription", str)
"""Описание мероприятия (String)"""

StrEventAddress = NewType("StrEventAddress", str)
"""Адрес мероприятия (String)"""
