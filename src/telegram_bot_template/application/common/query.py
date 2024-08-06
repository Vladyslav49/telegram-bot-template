from abc import ABC, abstractmethod


class Query[InputDTO, OutputDTO](ABC):
    __slots__ = ()

    @abstractmethod  # noqa: vulture
    async def __call__(self, data: InputDTO, /) -> OutputDTO:
        raise NotImplementedError


class QueryWithoutInput[OutputDTO](ABC):
    __slots__ = ()

    @abstractmethod  # noqa: vulture
    async def __call__(self) -> OutputDTO:
        raise NotImplementedError
