from datetime import timedelta
from typing import Any, Tuple, Type

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from app.utils.date_utils import parse_str_to_timedelta


class DotEnvCustomSource(DotEnvSettingsSource):
    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        value = super().prepare_field_value(field_name, field, value, value_is_complex)
        if not value:
            return
        return parse_str_to_timedelta(value)


class EnvCustomSource(EnvSettingsSource):
    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        value = super().prepare_field_value(field_name, field, value, value_is_complex)
        if not value:
            return
        return parse_str_to_timedelta(value)


class _Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DEBUG: bool
    DB_ENGINE: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    JWT_KEY: str
    JWT_ACCESS_EXPIRE: timedelta
    JWT_REFRESH_EXPIRE: timedelta

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (init_settings, EnvCustomSource(settings_cls), DotEnvCustomSource(settings_cls), file_secret_settings)


Config = _Config()  # type: ignore
