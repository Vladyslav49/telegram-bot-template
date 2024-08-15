import pytest

from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.enums.user_role import UserRole
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId


@pytest.fixture()
def user_entity() -> User:
    telegram_id = TelegramId(1)
    return User(telegram_id=telegram_id, role=UserRole.CLIENT)


def test_assign_administrator_role(user_entity: User) -> None:
    user_entity.assign_administrator_role()

    assert user_entity.is_administrator
