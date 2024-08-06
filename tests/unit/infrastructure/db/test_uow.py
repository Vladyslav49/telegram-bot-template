from unittest.mock import create_autospec

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot_template.application.common.exceptions import (
    CommitError,
    RollbackError,
)
from telegram_bot_template.infrastructure.db.uow import SQLAlchemyUnitOfWork


async def test_commit_raises_commit_error_on_sqlalchemy_error() -> None:
    session = create_autospec(AsyncSession)
    session.commit.side_effect = SQLAlchemyError  # noqa: vulture
    uow = SQLAlchemyUnitOfWork(session)

    with pytest.raises(CommitError):
        await uow.commit()


async def test_rollback_raises_rollback_error_on_sqlalchemy_error() -> None:
    session = create_autospec(AsyncSession)
    session.rollback.side_effect = SQLAlchemyError  # noqa: vulture
    uow = SQLAlchemyUnitOfWork(session)

    with pytest.raises(RollbackError):
        await uow.rollback()
