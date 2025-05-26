from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from .session import BaseModel


class Accounts(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, nullable=False) # Айди пользователя
    name = Column(String, unique=True, index=True, nullable=False) # Имя пользователя
    login = Column(String, unique=True, index=True, nullable=False) # Логин пользователя
    password_hash = Column(String) # Хеш пароля пользователя 

    events = relationship("Events", back_populates="creator")
    tickets = relationship("Tickets", back_populates="user")


class Events(BaseModel):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True) # Айди мероприятия
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False) # Айди пользователя, который создал мероприятие (users.id)
    title = Column(String) # Название мероприятия
    description = Column(String) # Полное описание мероприятия
    address = Column(String, nullable=False) # Адрес мероприятия
    datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now()) # Дата в формате 11:11 21.05.2025

    creator = relationship("Accounts", back_populates="events")
    ticket_types = relationship("TicketTypes", back_populates="event")
    tickets = relationship("Tickets", back_populates="event")


class TicketTypes(BaseModel):
    __tablename__ = 'ticket_types'

    id = Column(Integer, primary_key=True, index=True) # Айди билета (это тип. родитель.)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False) # Айди мероприятия, к которму относится билет (event.id)
    type = Column(String, nullable=False) # Тип билета (Vip, Standard, Econom)
    price = Column(Integer, nullable=False) # Цена билета
    total_count = Column(Integer, nullable=False) # Сколько всего таких билетов будет
    description = Column(String) # Описание билета

    event = relationship("Events", back_populates="ticket_types")


class Tickets(BaseModel):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True) # Айди билета (кьюаркода) (это сам билет)
    event_id = Column(Integer, ForeignKey('events.id'), index=True, nullable=False) # Айди мероприятия, на который куплен билет
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False) # Айди пользователя, который купил билет
    ticket_type_id = Column(Integer, ForeignKey('ticket_types.id'), index=True, nullable=False) # Тип билета (ticket_types.id)
    unique_code = Column(String, unique=True, nullable=False) # Уникальный код билета для кьюаркода
    is_used = Column(Boolean, default=False) # Активирован ли билет

    event = relationship("Events", back_populates="tickets")
    user = relationship("Accounts", back_populates="tickets")