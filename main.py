from fastapi import FastAPI

from app.config import Config

app = FastAPI(debug=Config.DEBUG)
