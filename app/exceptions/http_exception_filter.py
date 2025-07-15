from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def register_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(Exception)(unhandled_exception_filter)
    app.exception_handler(HTTPException)(http_exception_filter)
    app.exception_handler(RequestValidationError)(pyndndic_exception_filter)


def http_exception_filter(_: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"errors": [exc.detail]},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "errors": [
                    "Sorry something went wrong on our end!, Please try again later"
                ]
            },
        )


def unhandled_exception_filter(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "errors": ["Sorry something went wrong on our end!, Please try again later"]
        },
    )


def pyndndic_exception_filter(_: Request, exc: RequestValidationError) -> JSONResponse:
    # Need to look: https://docs.pydantic.dev/latest/errors/errors/#customize-error-messages # noqa: E501
    error_messages = [error["msg"] for error in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": error_messages if error_messages else ["Validation error"]},
    )
