from dataclasses import dataclass, field
from typing import final

from telegram_bot_template.domain.enums.user import UserRole
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.domain.value_objects.user_id import UserId


@final
@dataclass(kw_only=True, slots=True)
class User:
    id: UserId = field(init=False)
    telegram_id: TelegramId
    role: UserRole
