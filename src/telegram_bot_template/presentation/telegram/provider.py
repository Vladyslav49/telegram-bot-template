from aiogram.types import TelegramObject

from telegram_bot_template.application.common.id_provider import IdProvider
from telegram_bot_template.application.user.queries.get_user_id_by_telegram_id import (  # noqa: E501
    GetUserIdByTelegramId,
    GetUserIdByTelegramIdInputDTO,
)
from telegram_bot_template.infrastructure.auth.id_provider import RawIdProvider


async def get_id_provider(
    event: TelegramObject, get_user_id_by_telegram_id: GetUserIdByTelegramId
) -> IdProvider:
    if not hasattr(event, "from_user") or event.from_user is None:
        msg = "Event must have a non-null 'from_user' attribute"
        raise ValueError(msg)
    user_id = await get_user_id_by_telegram_id(
        GetUserIdByTelegramIdInputDTO(telegram_id=event.from_user.id)
    )
    return RawIdProvider(user_id)
