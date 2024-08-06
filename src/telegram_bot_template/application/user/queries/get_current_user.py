import logging
from typing import Final, final, override

from telegram_bot_template.application.common.db.user import (
    UserReader,
)
from telegram_bot_template.application.common.id_provider import IdProvider
from telegram_bot_template.application.common.query import QueryWithoutInput
from telegram_bot_template.application.user.exceptions import (
    UserIsNotExistsError,
)
from telegram_bot_template.domain.entities.user import User

logger: Final = logging.getLogger(__name__)


@final
class GetCurrentUser(QueryWithoutInput[User]):
    __slots__ = ("_user_reader", "_id_provider")

    def __init__(
        self,
        *,
        user_reader: UserReader,
        id_provider: IdProvider,
    ) -> None:
        self._user_reader = user_reader
        self._id_provider = id_provider

    @override
    async def __call__(self) -> User:
        user_id = self._id_provider.get_current_user_id()
        try:
            user = await self._user_reader.get_by_id(user_id)
        except UserIsNotExistsError:
            logger.error("User with ID %s does not exist", user_id.to_raw())  # noqa: TRY400
            raise
        logger.info("Successfully got user with ID %s", user_id.to_raw())
        return user
