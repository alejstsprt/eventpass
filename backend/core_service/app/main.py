import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core_service.app.api.v1 import event, ticket_types, tickets, user
from backend.core_service.app.middleware.cors import setup_cors
from backend.core_service.app.models.session import DBBaseModel, engine

DBBaseModel.metadata.create_all(bind=engine)

app = FastAPI()
setup_cors(app)


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
