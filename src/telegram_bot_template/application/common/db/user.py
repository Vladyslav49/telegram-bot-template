from abc import ABC, abstractmethod

from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.domain.value_objects.user_id import UserId


class UserSaver(ABC):
    __slots__ = ()

    @abstractmethod
    async def save(self, user: User, /) -> UserId:
        raise NotImplementedError


class UserReader(ABC):
    __slots__ = ()

    @abstractmethod
    async def get_by_id(self, id: UserId, /) -> User:
        raise NotImplementedError

    @abstractmethod
    async def acquire_by_id(self, id: UserId, /) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_id_by_telegram_id(
        self, telegram_id: TelegramId, /
    ) -> UserId:
        raise NotImplementedError

    @abstractmethod
    async def get_all_telegram_ids(self) -> tuple[TelegramId, ...]:
        raise NotImplementedError
