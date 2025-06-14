from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from backend.core_service.app.core.logger import logger_api


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response | JSONResponse:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger_api.exception(f"Ошибка сервера. {type(e).__name__}: {e}")
            return JSONResponse(
                {"message": "Ошибка. попробуйте позже."}, status_code=500
            )
