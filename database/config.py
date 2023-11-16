from sqlalchemy.ext.asyncio import create_async_engine

from app.config import Config

DSN = f"{Config.DB_ENGINE}://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

engine = create_async_engine(DSN)
