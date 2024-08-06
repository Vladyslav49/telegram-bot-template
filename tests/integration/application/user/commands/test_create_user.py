import pytest
from dishka import AsyncContainer

from telegram_bot_template.application.user.commands.create_user import (
    CreateUser,
    CreateUserInputDTO,
)
from telegram_bot_template.application.user.exceptions import (
    UserTelegramIdAlreadyExistsError,
)


@pytest.mark.usefixtures("user_id")
async def test_create_user_when_telegram_id_already_exists(
    container: AsyncContainer, telegram_id: int
) -> None:
    create_user = await container.get(CreateUser)

    with pytest.raises(UserTelegramIdAlreadyExistsError):
        await create_user(
            CreateUserInputDTO(telegram_id=telegram_id),
        )
