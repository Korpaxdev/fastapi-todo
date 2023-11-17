from fastapi import HTTPException, status

from app.utils.constants import Errors


class UserExistsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail=Errors.USER_IS_EXISTS)


class UserNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail=Errors.USER_NOT_FOUND)


class WrongTokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, Errors.WRONG_TOKEN)


class TokenExpiredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, Errors.EXPIRED_TOKEN)
