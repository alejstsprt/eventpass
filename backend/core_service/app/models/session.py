from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite:///./eventpass.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseModel(DeclarativeBase):
    """Класс-основа для создания моделей бд"""

    pass


def get_db() -> Generator[Session, None, None]:
    """Сессия БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
