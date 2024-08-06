import pytest
from dishka import AsyncContainer

from telegram_bot_template.application.user.exceptions import (
    UserIsNotExistsError,
)
from telegram_bot_template.application.user.queries.get_user_id_by_telegram_id import (  # noqa: E501
    GetUserIdByTelegramId,
    GetUserIdByTelegramIdInputDTO,
)
from telegram_bot_template.domain.value_objects.user_id import UserId


async def test_get_user_id_by_telegram_id(
    container: AsyncContainer, telegram_id: int, user_id: UserId
) -> None:
    get_user_id_by_telegram_id = await container.get(GetUserIdByTelegramId)

    result_user_id = await get_user_id_by_telegram_id(
        GetUserIdByTelegramIdInputDTO(telegram_id=telegram_id)
    )

    assert result_user_id == user_id


async def test_get_user_id_by_telegram_id_not_exists(
    container: AsyncContainer, telegram_id: int
) -> None:
    get_user_id_by_telegram_id = await container.get(GetUserIdByTelegramId)

    with pytest.raises(UserIsNotExistsError):
        await get_user_id_by_telegram_id(
            GetUserIdByTelegramIdInputDTO(telegram_id=telegram_id)
        )
