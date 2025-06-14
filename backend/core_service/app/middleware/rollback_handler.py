from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from backend.core_service.app.models.session import SessionLocal


class SQLAlchemySessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.db = SessionLocal()
        try:
            response = await call_next(request)
            request.state.db.commit()
            return response
        except SQLAlchemyError:
            request.state.db.rollback()
            raise
        except Exception:
            request.state.db.rollback()
            raise
        finally:
            request.state.db.close()
