import logging
from dataclasses import dataclass
from typing import Final, final, override

from telegram_bot_template.application.common.command import Command
from telegram_bot_template.application.common.db.user import (
    UserSaver,
)
from telegram_bot_template.application.common.uow import UnitOfWork
from telegram_bot_template.application.user.exceptions import (
    UserTelegramIdAlreadyExistsError,
)
from telegram_bot_template.domain.factories.user import UserFactory
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.domain.value_objects.user_id import UserId

logger: Final = logging.getLogger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class CreateUserInputDTO:
    telegram_id: int


@final
class CreateUser(Command[CreateUserInputDTO, UserId]):
    __slots__ = ("_user_saver", "_user_factory", "_uow")

    def __init__(
        self,
        *,
        user_saver: UserSaver,
        user_factory: UserFactory,
        uow: UnitOfWork,
    ) -> None:
        self._user_saver = user_saver
        self._user_factory = user_factory
        self._uow = uow

    @override  # noqa: vulture
    async def __call__(self, data: CreateUserInputDTO, /) -> UserId:
        async with self._uow:
            user = self._user_factory.create(
                telegram_id=TelegramId(data.telegram_id)
            )

            try:
                user_id = await self._user_saver.save(user)
            except UserTelegramIdAlreadyExistsError:
                logger.warning(
                    "User with Telegram ID %s already exists", data.telegram_id
                )
                raise

            await self._uow.commit()

        logger.info("User created with ID %s", user_id.to_raw())

        return user_id
