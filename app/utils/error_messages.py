from typing import NamedTuple


class Errors(NamedTuple):
    INVALID_PASSWORD = (
        "The password must have: at least one uppercase English letter,"
        "at least one lowercase English letter, at least one digit"
    )
    USER_IS_EXISTS = "A user with this email or username already exists"
    USER_NOT_FOUND = "A user with this username or this password not found. Please check your username or password"
    WRONG_TOKEN = "Wrong token. Please check your token"
    EXPIRED_TOKEN = "Token expired"
