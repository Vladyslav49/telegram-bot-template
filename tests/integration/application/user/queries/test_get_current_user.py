import pytest
from dishka import AsyncContainer

from telegram_bot_template.application.user.exceptions import (
    UserIsNotExistsError,
)
from telegram_bot_template.application.user.queries.get_current_user import (
    GetCurrentUser,
)
from telegram_bot_template.domain.value_objects.user_id import UserId


async def test_get_current_user(
    container: AsyncContainer, user_id: UserId
) -> None:
    get_current_user = await container.get(GetCurrentUser)

    current_user = await get_current_user()

    assert current_user.id == user_id


async def test_get_current_user_not_exists(container: AsyncContainer) -> None:
    get_current_user = await container.get(GetCurrentUser)

    with pytest.raises(UserIsNotExistsError):
        await get_current_user()
