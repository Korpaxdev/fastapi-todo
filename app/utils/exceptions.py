from typing import Optional

from fastapi import HTTPException, status

from app.utils.constants import Errors


class BaseHTTPException(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: Optional[str]

    def __init__(self) -> None:
        super().__init__(self.status_code, detail=self.detail)


class UserExistsException(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = Errors.USER_IS_EXISTS


class UserNotFoundException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = Errors.USER_NOT_FOUND


class WrongTokenException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = Errors.WRONG_TOKEN


class TokenExpiredException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = Errors.EXPIRED_TOKEN


class UnauthorizedException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = Errors.UNAUTHORIZED
