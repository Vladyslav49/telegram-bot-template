from abc import ABC, abstractmethod


class Command[InputDTO, OutputDTO](ABC):
    __slots__ = ()

    @abstractmethod  # noqa: vulture
    async def __call__(self, data: InputDTO, /) -> OutputDTO:
        raise NotImplementedError
