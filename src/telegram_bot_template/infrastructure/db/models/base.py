from typing import override

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    @override
    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return cls.__name__.lower().replace("model", "")
