from typing import final

from telegram_bot_template.domain.common.value_objects.base import ValueObject


@final
class TelegramId(ValueObject[int]):
    value: int
