from dataclasses import dataclass
from typing import final

from telegram_bot_template.domain.enums.user_role import UserRole
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.domain.value_objects.user_id import UserId


@final
@dataclass(kw_only=True, slots=True)
class User:
    id: UserId | None = None
    telegram_id: TelegramId
    role: UserRole

    @property
    def is_administrator(self) -> bool:
        return self.role is UserRole.ADMINISTRATOR

    def assign_administrator_role(self) -> None:
        self.role = UserRole.ADMINISTRATOR
