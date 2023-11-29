from datetime import datetime

from pydantic import BaseModel


class TodoBaseSchema(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    expired: datetime
    is_completed: bool
    is_expired: bool
