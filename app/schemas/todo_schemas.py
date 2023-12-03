from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field


class CreateTodoInputSchema(BaseModel):
    title: str
    description: Optional[str] = None
    expired: datetime = Field(examples=[datetime.now() + timedelta(days=10)])


class TodoResponseSchema(CreateTodoInputSchema):
    id: int
    created_at: datetime
    is_completed: bool
    is_expired: bool
