import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.constants import Errors


class BaseUserInputSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, examples=["MyTestPassword123"])

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        is_valid = bool(re.findall(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).*$", value))
        if not is_valid:
            raise ValueError(Errors.INVALID_PASSWORD)
        return value


class AccessTokenResponseSchema(BaseModel):
    ACCESS: str


class TokenResponseSchema(AccessTokenResponseSchema):
    REFRESH: str


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
