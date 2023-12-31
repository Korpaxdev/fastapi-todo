from app.schemas.todo_schemas import CreateTodoInputSchema
from database.config import sessionmaker
from database.models import TodoModel, UserModel


async def insert_todo(todo: CreateTodoInputSchema, user: UserModel):
    async with sessionmaker() as session:
        new_todo = TodoModel(**todo.__dict__, user_id=user.id)
        session.add(new_todo)
        await session.commit()
        return new_todo
