import logging
from dataclasses import dataclass
from typing import Final, final, override

from telegram_bot_template.application.common.command import Command
from telegram_bot_template.application.common.db.user import (
    UserReader,
    UserSaver,
)
from telegram_bot_template.application.common.uow import UnitOfWork
from telegram_bot_template.application.user.exceptions import (
    UserAlreadyHasAdminRoleError,
)
from telegram_bot_template.application.user.queries.get_current_user import (
    GetCurrentUser,
)
from telegram_bot_template.domain.exceptions.access import AccessDenied
from telegram_bot_template.domain.services.access import AccessService
from telegram_bot_template.domain.value_objects.user_id import UserId

logger: Final = logging.getLogger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class AssignAdministratorRoleInputDTO:
    user_id: int


@final
class AssignAdministratorRole(Command[AssignAdministratorRoleInputDTO, None]):
    __slots__ = (
        "_user_saver",
        "_user_reader",
        "_access_service",
        "_uow",
        "_get_current_user",
    )

    def __init__(
        self,
        *,
        user_saver: UserSaver,
        user_reader: UserReader,
        access_service: AccessService,
        uow: UnitOfWork,
        get_current_user: GetCurrentUser,
    ) -> None:
        self._user_saver = user_saver
        self._user_reader = user_reader
        self._access_service = access_service
        self._uow = uow
        self._get_current_user = get_current_user

    @override  # noqa: vulture
    async def __call__(self, data: AssignAdministratorRoleInputDTO, /) -> None:
        async with self._uow:
            current_user = await self._get_current_user()

            try:
                self._access_service.ensure_is_administrator(current_user)
            except AccessDenied:
                assert current_user.id is not None
                logger.warning(
                    "User with ID %s attempted to assign an administrator role but is not an administrator",  # noqa: E501
                    current_user.id.to_raw(),
                )
                raise

            user = await self._user_reader.acquire_by_id(UserId(data.user_id))

            if user.is_administrator:
                logger.warning(
                    "Attempt to assign administrator role to user with ID %s failed. User already has administrator role",  # noqa: E501
                    data.user_id,
                )
                raise UserAlreadyHasAdminRoleError

            user.assign_administrator_role()
            await self._user_saver.save(user)
            await self._uow.commit()

        assert current_user.id is not None

        logger.info(
            "Administrator role assigned to user with ID %s by user with ID %s",  # noqa: E501
            data.user_id,
            current_user.id.to_raw(),
        )
