from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, String, Text, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(DeclarativeBase):
    pass


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    todos: Mapped[list["TodoModel"]] = relationship(back_populates="user", lazy=False)

    def __str__(self) -> str:
        return f"User(email={self.email})"


class TodoModel(BaseModel):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, insert_default=func.now())
    expired: Mapped[datetime] = mapped_column(TIMESTAMP)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.id))
    user: Mapped[UserModel] = relationship(back_populates="todos", lazy=False)

    @hybrid_property
    def is_expired(self):
        return self.expired < datetime.now()
