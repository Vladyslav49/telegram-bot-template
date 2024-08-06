from abc import ABC, abstractmethod
from types import TracebackType
from typing import final


class UnitOfWork(ABC):
    __slots__ = ()

    @final
    async def __aenter__(self) -> None:
        return None

    @final
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
