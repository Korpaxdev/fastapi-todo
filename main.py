from fastapi import FastAPI

from app.config import Config
from routes.user_routes import user_router

app = FastAPI(debug=Config.DEBUG)
app.include_router(user_router)
