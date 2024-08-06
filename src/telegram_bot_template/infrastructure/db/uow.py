from typing import final, override

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot_template.application.common.exceptions import (
    CommitError,
    RollbackError,
)
from telegram_bot_template.application.common.uow import UnitOfWork


@final
class SQLAlchemyUnitOfWork(UnitOfWork):
    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession, /) -> None:  # noqa: vulture
        self._session = session

    @override
    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as e:
            raise CommitError from e

    @override
    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as e:
            raise RollbackError from e
