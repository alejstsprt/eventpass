from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .session import Base

class Accounts(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True) # Айди пользователя
    login = Column(String, unique=True, index=True) # Логин пользователя
    password_hash = Column(String) # Хеш пароля пользователя 

    events = relationship("Events", back_populates="creator")
    tickets = relationship("Tickets", back_populates="user")


class Events(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True) # Айди мероприятия
    creator_id = Column(Integer, ForeignKey('users.id')) # Айди пользователя, который создал мероприятие (users.id)
    title = Column(String) # Название мероприятия
    description = Column(String) # Полное описание мероприятия
    address = Column(String) # Адрес мероприятия
    datatime = Column(DateTime) # Дата в формате 11:11 21.05.2025

    creator = relationship("Accounts", back_populates="events")
    ticket_types = relationship("TicketTypes", back_populates="event")
    tickets = relationship("Tickets", back_populates="event")


class TicketTypes(Base):
    __tablename__ = 'ticket_types'

    id = Column(Integer, primary_key=True, index=True) # Айди билета (это тип. родитель.)
    event_id = Column(Integer, ForeignKey('events.id')) # Айди мероприятия, к которму относится билет (event.id)
    type = Column(String) # Тип билета (Vip, Standard, Econom)
    price = Column(Integer) # Цена билета
    total_count = Column(Integer) # Сколько всего таких билетов будет
    description = Column(String) # Описание билета

    event = relationship("Events", back_populates="ticket_types")


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True) # Айди билета (кьюаркода) (это сам билет)
    event_id = Column(Integer, ForeignKey('events.id'), index=True) # Айди мероприятия, на который куплен билет
    user_id = Column(Integer, ForeignKey('users.id'), index=True) # Айди пользователя, который купил билет
    ticket_type_id = Column(Integer, ForeignKey('ticket_types.id'), index=True) # Тип билета (ticket_types.id)
    unique_code = Column(String, unique=True) # Уникальный код билета для кьюаркода
    is_used = Column(Boolean, default=False) # Активирован ли билет

    event = relationship("Events", back_populates="tickets")
    user = relationship("Accounts", back_populates="tickets")