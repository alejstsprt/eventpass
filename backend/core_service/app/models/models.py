from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from models.session import DBBaseModel


class Accounts(DBBaseModel):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, index=True, nullable=False
    )  # Айди пользователя
    name = Column(String, unique=True, index=True, nullable=False)  # Имя пользователя
    login = Column(
        String, unique=True, index=True, nullable=False
    )  # Логин пользователя
    password_hash = Column(String)  # Хеш пароля пользователя

    events = relationship("Events", back_populates="creator")
    tickets = relationship("Tickets", back_populates="user")


class Events(DBBaseModel):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)  # Айди мероприятия
    creator_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Айди пользователя, который создал мероприятие (users.id)
    status = Column(
        String, nullable=False
    )  # Статус мероприятия (опубликовано/завершено/черновик).
    category = Column(String, nullable=False)
    title = Column(String, nullable=False)  # Название мероприятия
    description = Column(String, nullable=False)  # Полное описание мероприятия
    address = Column(String, nullable=False)  # Адрес мероприятия
    datetime = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )  # Дата в формате 11:11 21.05.2025
    # end_datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now()) # Дата в формате 11:11 21.05.2025 # TODO: сделать

    creator = relationship("Accounts", back_populates="events")
    ticket_types = relationship("TicketTypes", back_populates="event")
    tickets = relationship("Tickets", back_populates="event")


class TicketTypes(DBBaseModel):
    """Это тип билета (вип и тд)"""

    __tablename__ = "ticket_types"

    id = Column(
        Integer, primary_key=True, index=True
    )  # Айди билета (это тип. родитель.)
    event_id = Column(
        Integer, ForeignKey("events.id"), nullable=False
    )  # Айди мероприятия, к которму относится билет (event.id)
    type = Column(String, nullable=False)  # Тип билета (Vip, Standard, Econom)
    description = Column(String)  # Описание билета
    price = Column(Integer, nullable=False)  # Цена билета
    total_count = Column(Integer, nullable=False)  # Сколько всего таких билетов будет

    event = relationship("Events", back_populates="ticket_types")
    ticket = relationship("Tickets", back_populates="ticket_type")


class Tickets(DBBaseModel):
    """Сами билеты"""

    __tablename__ = "tickets"

    id = Column(
        Integer, primary_key=True, index=True
    )  # Айди билета (кьюаркода) (это сам билет)
    event_id = Column(
        Integer, ForeignKey("events.id"), index=True, nullable=False
    )  # Айди мероприятия, на который куплен билет
    user_id = Column(
        Integer, ForeignKey("users.id"), index=True, nullable=False
    )  # Айди пользователя, который купил билет
    ticket_type_id = Column(
        Integer, ForeignKey("ticket_types.id"), index=True, nullable=False
    )  # Тип билета (ticket_types.id)
    unique_code = Column(
        String, unique=True, nullable=False
    )  # Уникальный код билета для кьюаркода
    is_used = Column(Boolean, default=False)  # Активирован ли билет

    event = relationship("Events", back_populates="tickets")
    user = relationship("Accounts", back_populates="tickets")
    ticket_type = relationship("TicketTypes", back_populates="ticket")
