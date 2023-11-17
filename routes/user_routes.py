from fastapi import APIRouter
from sqlalchemy import or_

from app.schemas.user_schemas import BaseUserSchema, TokenResponseSchema, UserResponseSchema
from app.services.user_services import check_user_exists, find_user, insert_user
from app.utils.exceptions import UserExistsException, UserNotFoundException
from app.utils.password_utils import check_password
from app.utils.token_utils import generate_access_token, generate_refresh_token
from database.models import UserModel

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserResponseSchema)
async def register_user(user_data: BaseUserSchema):
    if await check_user_exists(user_data):
        raise UserExistsException
    return await insert_user(user_data)


@user_router.post("/token", response_model=TokenResponseSchema)
async def get_token(user_data: BaseUserSchema):
    user = await find_user(or_(UserModel.email == user_data.email))
    if not user or not check_password(user_data.password, user.hashed_password):
        raise UserNotFoundException
    token_data = {"id": user.id}
    return TokenResponseSchema(access=generate_access_token(token_data), refresh=generate_refresh_token(token_data))
