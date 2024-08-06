from dataclasses import dataclass
from typing import Any, final


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class RedisConfig:
    dsn: str


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class LoggingConfig:
    config: dict[str, Any]
