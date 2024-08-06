from abc import ABC
from dataclasses import dataclass
from typing import final


@dataclass(frozen=True)
class BaseValueObject(ABC):  # noqa: B024
    @final
    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:  # noqa: B027
        pass


@dataclass(frozen=True)
class ValueObject[T](BaseValueObject, ABC):
    value: T

    @final
    def to_raw(self) -> T:
        return self.value
