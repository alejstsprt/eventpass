import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import event, ticket_types, tickets, user
from .models.session import BaseModel, engine

BaseModel.metadata.create_all(bind=engine)

app = FastAPI()

# Разрешаем запросы с вашего фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
        "http://192.168.0.104",  # Добавьте ваш IP-адрес
        "http://192.168.0.104:8000",  # И порт, если используется
    ],  # И адреса
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user.router,
    prefix="/api/v1/auth",
    tags=["Ручки для взаимодействия с профилем пользователя"],
)
app.include_router(
    event.router,
    prefix="/api/v1/events",
    tags=["Ручки для управления мероприятиями"],
)
app.include_router(
    ticket_types.router,
    prefix="/api/v1/ticket-types",
    tags=["Ручки для управления типом мероприятий"],
)
app.include_router(
    tickets.router, prefix="/api/v1/ticket", tags=["Ручки для управления билетами"]
)


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)

# python -m venv venv
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# venv\Scripts\activate || venv\Scripts\activate.bat
# uvicorn backend.core_service.app.main:app --host 192.168.0.104 --port 8000 --reload
# ipconfig

# tasklist | findstr uvicorn
# taskkill /PID 12476 /F
