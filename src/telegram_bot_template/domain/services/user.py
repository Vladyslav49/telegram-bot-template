from typing import final

from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.enums.user import UserRole
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId


@final
class UserService:
    __slots__ = ()

    def create(self, *, telegram_id: TelegramId) -> User:
        return User(telegram_id=telegram_id, role=UserRole.CLIENT)

    def assign_admin_role(self, user: User, /) -> None:
        user.role = UserRole.ADMINISTRATOR
