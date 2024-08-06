import pytest
from dishka import AsyncContainer

from telegram_bot_template.application.user.queries.get_all_telegram_ids import (  # noqa: E501
    GetAllTelegramIds,
)
from telegram_bot_template.domain.exceptions.access import AccessDenied


@pytest.mark.usefixtures("make_user_admin")
async def test_get_all_telegram_ids_as_administrator(
    container: AsyncContainer, telegram_id: int
) -> None:
    get_all_telegram_ids = await container.get(GetAllTelegramIds)

    telegram_ids = await get_all_telegram_ids()

    assert len(telegram_ids) == 1
    assert telegram_ids[0].to_raw() == telegram_id


@pytest.mark.usefixtures("user_id")
async def test_get_all_telegram_ids_as_client(
    container: AsyncContainer,
) -> None:
    get_all_telegram_ids = await container.get(GetAllTelegramIds)

    with pytest.raises(AccessDenied):
        await get_all_telegram_ids()
