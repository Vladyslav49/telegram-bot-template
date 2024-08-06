import logging
from typing import Final, final, override

from telegram_bot_template.application.common.db.user import (
    UserReader,
)
from telegram_bot_template.application.common.query import QueryWithoutInput
from telegram_bot_template.application.user.queries.get_current_user import (
    GetCurrentUser,
)
from telegram_bot_template.domain.exceptions.access import AccessDenied
from telegram_bot_template.domain.services.access import AccessService
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId

logger: Final = logging.getLogger(__name__)


@final
class GetAllTelegramIds(QueryWithoutInput[tuple[TelegramId, ...]]):
    __slots__ = ("_user_reader", "_access_service", "_get_current_user")

    def __init__(
        self,
        *,
        user_reader: UserReader,
        access_service: AccessService,
        get_current_user: GetCurrentUser,
    ) -> None:
        self._user_reader = user_reader
        self._access_service = access_service
        self._get_current_user = get_current_user

    @override  # noqa: vulture
    async def __call__(self) -> tuple[TelegramId, ...]:
        current_user = await self._get_current_user()
        try:
            self._access_service.ensure_is_administrator(current_user)
        except AccessDenied:
            logger.warning(
                "User with ID %s attempted to get all user IDs but is not an administrator",  # noqa: E501
                current_user.id.to_raw(),
            )
            raise
        return await self._user_reader.get_all_telegram_ids()
