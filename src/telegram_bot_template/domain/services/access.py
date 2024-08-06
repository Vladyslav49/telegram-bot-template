from typing import final

from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.enums.user import UserRole
from telegram_bot_template.domain.exceptions.access import AccessDenied


@final
class AccessService:
    __slots__ = ()

    def ensure_is_administrator(self, user: User, /) -> None:
        if not self.is_administrator(user):
            raise AccessDenied

    def is_administrator(self, user: User, /) -> bool:
        return user.role is UserRole.ADMINISTRATOR
