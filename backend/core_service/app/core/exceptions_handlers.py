from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = []

    for err in exc.errors():
        errors.append(err.get("msg"))

    return JSONResponse(
        content={"errors": errors},
        status_code=422,
    )


async def rate_limit(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        content={"error": "Слишком много запросов. Попробуйте позже."},
        status_code=429,
    )
