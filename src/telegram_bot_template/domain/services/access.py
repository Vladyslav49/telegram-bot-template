from typing import final

from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.exceptions.access import AccessDenied


@final
class AccessService:
    __slots__ = ()

    def ensure_is_administrator(self, user: User, /) -> None:
        if not user.is_administrator:
            raise AccessDenied
