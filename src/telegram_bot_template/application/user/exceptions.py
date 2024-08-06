from typing import final

from telegram_bot_template.application.common.exceptions import (
    ApplicationError,
)


@final
class UserTelegramIdAlreadyExistsError(ApplicationError):
    pass


@final
class UserIsNotExistsError(ApplicationError):
    pass


@final
class UserAlreadyHasAdminRoleError(ApplicationError):
    pass
