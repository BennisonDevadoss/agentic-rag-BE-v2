from fastapi import HTTPException, status


class UnprocessableEntityException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message,
        )


class UnauthorizedException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class InternalServerException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
        )


class NotFoundException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class UnsupportedMediaTypeException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=message,
        )


class RequestTooLargeException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=message,
        )


class BadRequestException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class ServiceUnavailableException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=message
        )


class ConflictException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=message)


class PaymentRequiredException(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=message)


class ForbiddenException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class TooManyRequestsException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=message)
