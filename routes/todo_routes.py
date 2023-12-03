from typing import Annotated

from fastapi import APIRouter, Depends

from app.depends.user_depends import get_current_user_dependency
from app.schemas.todo_schemas import CreateTodoInputSchema, TodoResponseSchema
from app.services.todo_services import insert_todo
from database.models import UserModel

todo_router = APIRouter(prefix="/todos", tags=["To Do"])

UserType = Annotated[UserModel, Depends(get_current_user_dependency)]


@todo_router.get("/", response_model=list[TodoResponseSchema])
async def get_todos(user: UserType):
    return user.todos


@todo_router.post("/", response_model=TodoResponseSchema)
async def add_todo(todo: CreateTodoInputSchema, user: UserType):
    return await insert_todo(todo, user)
