from fastapi import HTTPException, status

from app.utils.error_messages import Errors


class UserExistsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail=Errors.USER_IS_EXISTS)
