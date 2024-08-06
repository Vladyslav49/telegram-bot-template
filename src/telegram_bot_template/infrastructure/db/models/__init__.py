from telegram_bot_template.infrastructure.db.models.base import Base
from telegram_bot_template.infrastructure.db.models.user import (
    UserModel,
)

__all__ = ("Base", "UserModel")
