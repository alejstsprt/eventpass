from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .api.v1 import user, user_tickets, events_organizer
from .models.session import Base, engine
from .models.models import Accounts, Events, TicketTypes, Tickets


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Разрешаем запросы с вашего фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost",
        "http://localhost:8000",
        "http://192.168.0.104",  # Добавьте ваш IP-адрес
        "http://192.168.0.104:8000"  # И порт, если используется
    ], # И адреса
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix='/api/user', tags=['🔐 Ручки для взаимодействия с профилем пользователя'])
# app.include_router(user_tickets.router, prefix='/api/tickets')
# app.include_router(events_organizer.router, prefix='/api/events')

# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)

# python -m venv venv
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# venv\Scripts\activate || venv\Scripts\activate.bat
# uvicorn backend.core-service.app.main:app --host 192.168.0.104 --port 8000 --reload
# ipconfig

# tasklist | findstr uvicorn
# taskkill /PID 12476 /F