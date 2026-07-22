from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import CSMSException
from app.common.responses import create_error_response
import logging

logger = logging.getLogger(__name__)


async def custom_exception_handler(request: Request, exc: CSMSException):
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(message=exc.message)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(l) for l in err.get("loc", [])])
        errors.append({
            "field": loc,
            "message": err.get("msg"),
            "type": err.get("type")
        })

    return JSONResponse(
        status_code=422,
        content=create_error_response(message="Validation Error", errors=errors)
    )
