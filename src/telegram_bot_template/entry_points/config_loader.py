import os
import tomllib
from pathlib import Path
from typing import Any, final

import yaml
from aiogram.utils.token import validate_token
from pydantic import PostgresDsn, RedisDsn, TypeAdapter

from telegram_bot_template.entry_points.config import (
    LoggingConfig,
    RedisConfig,
)
from telegram_bot_template.infrastructure.db.config import (
    DatabaseConfig,
)
from telegram_bot_template.presentation.telegram.config import TelegramConfig


def load_database_config() -> DatabaseConfig:
    dsn = _get_str_env("DATABASE_DSN")

    config_path = _get_str_env("CONFIG_PATH")
    config = _load_toml_config(Path(config_path))

    try:
        pool_size = config["database"]["pool_size"]
    except KeyError as e:
        msg = f"{e.args[0]} is not set"
        raise ConfigParseError(msg) from e

    postgres_dsn_adapter = TypeAdapter(PostgresDsn)
    postgres_dsn_adapter.validate_python(dsn)

    config_adapter = TypeAdapter(DatabaseConfig)

    return config_adapter.validate_python(
        DatabaseConfig(dsn=str(dsn), pool_size=pool_size), from_attributes=True
    )


def load_redis_config() -> RedisConfig:
    dsn = _get_str_env("REDIS_DSN")

    redis_dsn_adapter = TypeAdapter(RedisDsn)
    redis_dsn_adapter.validate_python(dsn)

    return RedisConfig(dsn=str(dsn))


def load_telegram_config() -> TelegramConfig:
    bot_api_token = _get_str_env("TELEGRAM_BOT_API_TOKEN")

    validate_token(bot_api_token)

    return TelegramConfig(bot_api_token=bot_api_token)


def load_logging_config() -> LoggingConfig:
    config_path = _get_str_env("LOGGING_CONFIG_PATH")
    config = _load_yaml_config(Path(config_path))
    return LoggingConfig(config=config)


def _get_str_env(key: str) -> str:
    try:
        return os.environ[key]
    except KeyError as e:
        msg = f"{key} is not set"
        raise ConfigParseError(msg) from e


@final
class ConfigParseError(ValueError):
    pass


def _load_toml_config(config_path: Path) -> dict[str, Any]:
    with config_path.open("rb") as file:
        return tomllib.load(file)


def _load_yaml_config(config_path: Path) -> dict[str, Any]:
    with config_path.open() as file:
        return yaml.safe_load(file)  # type: ignore[no-any-return]
