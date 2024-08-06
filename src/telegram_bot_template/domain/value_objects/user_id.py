from typing import final

from telegram_bot_template.domain.common.value_objects.base import ValueObject


@final
class UserId(ValueObject[int]):
    value: int
