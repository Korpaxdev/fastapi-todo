import json
from datetime import datetime
from typing import Any, Optional

from jose import jwt

from app.config import Config
from app.utils.constants import TokenTypes

type TokenDataType = Optional[dict[str, Any]]


def generate_token(data: TokenDataType, type: TokenTypes, expire: datetime):
    token_body = {"type": type.name, "exp": expire}
    if data:
        token_body["sub"] = json.dumps(data)
    return jwt.encode(token_body, Config.JWT_KEY)


def generate_access_token(data: TokenDataType = None):
    expire = datetime.utcnow() + Config.JWT_ACCESS_EXPIRE
    return generate_token(data, TokenTypes.ACCESS, expire)


def generate_refresh_token(data: TokenDataType = None):
    expire = datetime.utcnow() + Config.JWT_REFRESH_EXPIRE
    return generate_token(data, TokenTypes.REFRESH, expire)


def decode_token(token: str):
    return jwt.decode(token, Config.JWT_KEY)


def decode_sub(sub: Optional[str] = None) -> dict[str, Any] | None:
    if not sub:
        return None
    return json.loads(sub)
