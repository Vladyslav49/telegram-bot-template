import pytest

from telegram_bot_template.domain.enums.user_role import UserRole
from telegram_bot_template.domain.factories.user import UserFactory
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId


@pytest.fixture(scope="module")
def user_factory() -> UserFactory:
    return UserFactory()


def test_create(user_factory: UserFactory) -> None:
    telegram_id = TelegramId(1)

    user = user_factory.create(telegram_id=telegram_id)

    assert user.telegram_id == telegram_id
    assert user.role is UserRole.CLIENT
