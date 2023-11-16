from fastapi import APIRouter

from app.schemas.user_schemas import BaseUserSchema, UserResponseSchema
from app.services.user_services import check_user_exists, insert_user
from app.utils.exceptions import UserExistsException

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserResponseSchema)
async def register_user(user_data: BaseUserSchema):
    if await check_user_exists(user_data):
        raise UserExistsException
    return await insert_user(user_data)
