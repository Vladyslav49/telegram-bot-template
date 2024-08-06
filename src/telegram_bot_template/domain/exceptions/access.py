from typing import final

from telegram_bot_template.domain.exceptions.base import DomainError


@final
class AccessDenied(DomainError):  # noqa: N818
    pass
