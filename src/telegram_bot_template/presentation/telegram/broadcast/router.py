from typing import Final

from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram_broadcaster import Broadcaster
from aiogram_broadcaster.contents import TextContent
from aiogram_i18n import I18nContext
from dishka import FromDishka

from telegram_bot_template.application.user.queries.get_all_telegram_ids import (  # noqa: E501
    GetAllTelegramIds,
)
from telegram_bot_template.domain.exceptions.access import AccessDenied

ROUTER: Final = Router(name=__name__)


@ROUTER.message(Command("broadcast"))
async def on_broadcast(
    message: Message,
    command: CommandObject,
    i18n: I18nContext,
    get_all_telegram_ids: FromDishka[GetAllTelegramIds],
    broadcaster: Broadcaster,
    bot: Bot,
) -> None:
    try:
        telegram_ids = await get_all_telegram_ids()
    except AccessDenied:
        await message.answer(i18n.access.denied())
        return

    if not command.args:
        await message.answer(i18n.broadcast.error.no.message())
        return

    mailer = await broadcaster.create_mailer(
        TextContent(text=command.args),
        chats=[telegram_id.to_raw() for telegram_id in telegram_ids],
        bot=bot,
    )
    mailer.start()
