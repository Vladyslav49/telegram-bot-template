from enum import Enum, unique
from typing import final


@final
@unique
class UserRole(Enum):
    CLIENT = "CLIENT"
    ADMINISTRATOR = "ADMINISTRATOR"
