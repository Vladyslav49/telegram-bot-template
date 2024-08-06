from abc import ABC, abstractmethod

from telegram_bot_template.domain.value_objects.user_id import UserId


class IdProvider(ABC):
    __slots__ = ()

    @abstractmethod
    def get_current_user_id(self) -> UserId:
        raise NotImplementedError
