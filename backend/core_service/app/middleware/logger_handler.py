import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from backend.core_service.app.core.logger import logger_api


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration = round(time.perf_counter() - start, 5)
        logger_api.info(
            f"{request.method} {request.url.path} -> {response.status_code} [{duration}s]"
        )
        return response
