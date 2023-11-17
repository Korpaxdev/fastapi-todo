import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.error_messages import Errors


class BaseUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, examples=["MyTestPassword123"])

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        is_valid = bool(re.findall(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).*$", value))
        if not is_valid:
            raise ValueError(Errors.INVALID_PASSWORD)
        return value


class AccessTokeSchema(BaseModel):
    access: str


class RefreshTokenSchema(BaseModel):
    refresh: str


class TokenResponseSchema(AccessTokeSchema, RefreshTokenSchema):
    pass


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
