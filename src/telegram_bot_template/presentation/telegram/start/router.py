from contextlib import suppress
from typing import Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka

from telegram_bot_template.application.user.commands.create_user import (
    CreateUser,
    CreateUserInputDTO,
)
from telegram_bot_template.application.user.exceptions import (
    UserTelegramIdAlreadyExistsError,
)
from telegram_bot_template.presentation.telegram.start.state import StartSG

ROUTER: Final = Router(name=__name__)


@ROUTER.message(CommandStart())
async def on_start(
    message: Message,
    dialog_manager: DialogManager,
    create_user: FromDishka[CreateUser],
) -> None:
    assert message.from_user is not None

    with suppress(UserTelegramIdAlreadyExistsError):
        await create_user(
            CreateUserInputDTO(telegram_id=message.from_user.id),
        )

    await dialog_manager.start(StartSG.menu, mode=StartMode.RESET_STACK)
