from pydantic_settings import BaseSettings, SettingsConfigDict


class _Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DEBUG: bool
    DB_ENGINE: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int


Config = _Config()  # type: ignore
