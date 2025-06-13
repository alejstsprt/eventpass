from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.core_service.app.core.logger import logger_api


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger_api.exception(f"Ошибка сервера. {type(e).__name__}: {e}")
            return JSONResponse(
                status_code=500,
                content={"message": "Ошибка, попробуйте позже"},
            )
