from typing import Annotated, Any

from fastapi import Depends, Request, Security
from fastapi.security import APIKeyHeader
from jose import ExpiredSignatureError, JWTError

from app.services.user_services import find_user
from app.utils.constants import TokenTypes
from app.utils.exceptions import UnauthorizedException
from app.utils.token_utils import decode_token_with_sub, is_valid_token
from database.models import UserModel

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

type TokenType = dict[str, Any]


async def get_access_token_dependency(request: Request, authorization: str = Security(api_key_header)):
    try:
        token = authorization or request.cookies.get(TokenTypes.ACCESS.value)
        if not token:
            raise UnauthorizedException
        decoded = decode_token_with_sub(token)
        if not is_valid_token(TokenTypes.ACCESS, decoded):
            raise UnauthorizedException
        return decoded
    except (JWTError, ExpiredSignatureError):
        raise UnauthorizedException


async def get_refresh_token_dependency(request: Request, authorization: str = Security(api_key_header)):
    try:
        token = authorization or request.cookies.get(TokenTypes.REFRESH.value)
        if not token:
            raise UnauthorizedException
        decoded = decode_token_with_sub(token)
        if not is_valid_token(TokenTypes.REFRESH, decoded):
            raise UnauthorizedException
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
