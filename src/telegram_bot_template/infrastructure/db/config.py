from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class DatabaseConfig:
    dsn: str
    pool_size: int
