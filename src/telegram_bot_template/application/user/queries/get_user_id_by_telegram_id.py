import logging
from dataclasses import dataclass
from typing import Final, final, override

from telegram_bot_template.application.common.db.user import (
    UserReader,
)
from telegram_bot_template.application.common.query import Query
from telegram_bot_template.application.user.exceptions import (
    UserIsNotExistsError,
)
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.domain.value_objects.user_id import UserId

logger: Final = logging.getLogger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class GetUserIdByTelegramIdInputDTO:
    telegram_id: int


@final
class GetUserIdByTelegramId(Query[GetUserIdByTelegramIdInputDTO, UserId]):
    __slots__ = ("_user_reader",)

    def __init__(
        self,
        *,
        user_reader: UserReader,
    ) -> None:
        self._user_reader = user_reader

    @override  # noqa: vulture
    async def __call__(self, data: GetUserIdByTelegramIdInputDTO, /) -> UserId:
        try:
            user_id = await self._user_reader.get_id_by_telegram_id(
                TelegramId(data.telegram_id)
            )
        except UserIsNotExistsError:
            logger.error(  # noqa: TRY400
                "Could not get user ID for Telegram ID %s: no user found with this Telegram ID",  # noqa: E501
                data.telegram_id,
            )
            raise
        logger.info(
            "Successfully got user ID %s for Telegram ID %s",
            user_id.to_raw(),
            data.telegram_id,
        )
        return user_id
