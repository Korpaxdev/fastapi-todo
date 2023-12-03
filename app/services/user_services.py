from sqlalchemy import ColumnExpressionArgument, select

from app.schemas.user_schemas import BaseUserInputSchema
from app.utils.password_utils import hash_password
from database.config import sessionmaker
from database.models import UserModel


async def insert_user(user_data: BaseUserInputSchema) -> UserModel:
    user_data_dict = user_data.__dict__.copy()
    del user_data_dict["password"]
    user_data_dict["hashed_password"] = hash_password(user_data.password)
    async with sessionmaker() as session:
        new_user = UserModel(**user_data_dict)
        session.add(new_user)
        await session.commit()
        return new_user


async def find_user(criteria: ColumnExpressionArgument[bool]) -> UserModel | None:
    async with sessionmaker() as session:
        return await session.scalar(select(UserModel).filter(criteria))


async def check_user_exists(user_data: BaseUserInputSchema) -> bool:
    return bool(await find_user(UserModel.email == user_data.email))
