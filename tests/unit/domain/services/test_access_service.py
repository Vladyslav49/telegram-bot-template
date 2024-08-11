from contextlib import AbstractContextManager, nullcontext

import pytest

from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.enums.user_role import UserRole
from telegram_bot_template.domain.exceptions.access import AccessDenied
from telegram_bot_template.domain.services.access import AccessService
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId


@pytest.fixture(scope="module")
def access_service() -> AccessService:
    return AccessService()


@pytest.mark.parametrize(
    ("role", "contextmanager"),
    [
        (UserRole.CLIENT, pytest.raises(AccessDenied)),
        (UserRole.ADMINISTRATOR, nullcontext()),
    ],
)
def test_ensure_is_administrator(
    role: UserRole,
    contextmanager: AbstractContextManager,  # type: ignore[type-arg]
    access_service: AccessService,
) -> None:
    user = User(telegram_id=TelegramId(1), role=role)

    with contextmanager:
        access_service.ensure_is_administrator(user)
