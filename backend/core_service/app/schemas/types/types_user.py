from typing import NewType

# [User]
IntUserId = NewType("IntUserId", int)
"""Уникальный айди пользователя (Integer)"""

StrUserName = NewType("StrUserName", str)
"""Уникальное имя пользователя (String)"""

StrUserLogin = NewType("StrUserLogin", str)
"""Уникальный логин пользователя (String)"""

StrUserPassword = NewType("StrUserPassword", str)
"""Уникальный пароль пользователя (String)"""
