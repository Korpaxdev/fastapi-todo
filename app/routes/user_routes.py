from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response
from sqlalchemy import or_

from app.depends.user_depends import get_refresh_token_dependency
from app.schemas.user_schemas import (
    AccessTokenResponseSchema,
    BaseUserInputSchema,
    TokenResponseSchema,
    UserResponseSchema,
)
from app.services.user_services import check_user_exists, find_user, insert_user
from app.utils.exceptions import UserExistsException, UserNotFoundException, WrongTokenException
from app.utils.password_utils import check_password
from app.utils.token_utils import generate_access_token, generate_refresh_token
from database.models import UserModel

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserResponseSchema)
async def register_user(user_data: BaseUserInputSchema):
    """Register user route"""
    if await check_user_exists(user_data):
        raise UserExistsException
    return await insert_user(user_data)


@user_router.post("/token", response_model=TokenResponseSchema)
async def get_token(response: Response, user_data: BaseUserInputSchema):
    """Route for getting access and refresh tokens"""
    user = await find_user(or_(UserModel.email == user_data.email))
    if not user or not check_password(user_data.password, user.hashed_password):
        raise UserNotFoundException
    token_data = {"id": user.id}
    token = TokenResponseSchema(ACCESS=generate_access_token(token_data), REFRESH=generate_refresh_token(token_data))
    response.set_cookie("ACCESS", token.ACCESS)
    response.set_cookie("REFRESH", token.REFRESH)
    return token


@user_router.post("/token/refresh", response_model=AccessTokenResponseSchema)
async def get_access_token(token: Annotated[dict[str, Any], Depends(get_refresh_token_dependency)]):
    """Route for getting access token by refresh token. You need to log in"""
    user = await find_user(UserModel.id == token["sub"].get("id"))
    if not user:
        raise WrongTokenException
    token_data = {"id": user.id}
    return AccessTokenResponseSchema(ACCESS=generate_access_token(token_data))
