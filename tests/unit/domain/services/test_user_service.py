import pytest

from parser_bot.domain.entities.user import User
from parser_bot.domain.enums.user_role import UserRole
from parser_bot.domain.services.user import UserService
from parser_bot.domain.value_objects.telegram_id import TelegramId


@pytest.fixture(scope="module")
def user_service() -> UserService:
    return UserService()


def test_create(user_service: UserService) -> None:
    telegram_id = TelegramId(1)

    user = user_service.create(telegram_id=telegram_id)

    assert user.telegram_id == telegram_id
    assert user.role is UserRole.CLIENT


def test_assign_admin_role(user_service: UserService) -> None:
    user = User(telegram_id=TelegramId(1), role=UserRole.CLIENT)

    user_service.assign_admin_role(user)

    assert user.role is UserRole.ADMINISTRATOR
