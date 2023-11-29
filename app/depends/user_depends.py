from typing import Annotated, Any

from fastapi import Depends, Request, Security
from fastapi.security import APIKeyHeader
from jose import ExpiredSignatureError, JWTError

from app.services.user_services import find_user
from app.utils.exceptions import UnauthorizedException
from app.utils.token_utils import decode_sub, decode_token
from database.models import UserModel

type TokenType = dict[str, Any]

api_key_header = APIKeyHeader(name="Authorization")


async def get_access_token_dependency(request: Request, authorization: str = Security(api_key_header)) -> TokenType:
    try:
        token = authorization or request.cookies.get("access")
        if not token:
            raise UnauthorizedException
        decoded = decode_token(token)
        decoded["sub"] = decode_sub(decoded.get("sub"))
        return decoded
    except (JWTError, ExpiredSignatureError):
        raise UnauthorizedException


async def get_current_user_dependency(token: Annotated[TokenType, Depends(get_access_token_dependency)]) -> UserModel:
    sub = token.get("sub")
    if not sub or not sub.get("id"):
        raise UnauthorizedException
    user = await find_user(UserModel.id == sub.get("id"))
    if not user:
        raise UnauthorizedException
    return user
