from app.api.v1 import events, users
from app.core.lifespan import lifespan
from fastapi import FastAPI
import uvicorn

app = FastAPI(lifespan=lifespan)

app.include_router(
    users.router, prefix="/api/v1/users", tags=["Ручки для работы с напоминаниями"]
)
app.include_router(
    events.router, prefix="/api/v1/events", tags=["Ручки для работы с мероприятиями"]
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.0.104", port=8100, reload=True)
