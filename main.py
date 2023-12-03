from fastapi import FastAPI

from app.config import Config
from app.routes.todo_routes import todo_router
from app.routes.user_routes import user_router

app = FastAPI(debug=Config.DEBUG)
app.include_router(user_router)
app.include_router(todo_router)
