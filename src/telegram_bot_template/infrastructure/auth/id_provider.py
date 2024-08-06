from typing import final, override

from telegram_bot_template.application.common.id_provider import IdProvider
from telegram_bot_template.domain.value_objects.user_id import UserId


@final
class RawIdProvider(IdProvider):
    __slots__ = ("_user_id",)

    def __init__(  # noqa: vulture
        self,
        user_id: UserId,
        /,
    ) -> None:
        self._user_id = user_id

    @override
    def get_current_user_id(self) -> UserId:
        return self._user_id
