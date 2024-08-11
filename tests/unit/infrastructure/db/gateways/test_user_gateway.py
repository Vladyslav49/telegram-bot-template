from unittest.mock import create_autospec

import pytest
from psycopg.errors import Diagnostic, UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot_template.application.common.exceptions import SaverError
from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.enums.user_role import UserRole
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.infrastructure.db.gateways.user import UserSaverImpl


async def test_save_raises_saver_error_on_integrity_error_other_than_unique_constraint() -> (  # noqa: E501
    None
):
    session = create_autospec(AsyncSession)
    orig = create_autospec(UniqueViolation)
    orig.diag = create_autospec(Diagnostic)
    orig.diag.constraint_name = "some_other_constraint"
    session.flush.side_effect = IntegrityError(  # noqa: vulture
        orig=orig, statement=None, params=None
    )
    user_saver = UserSaverImpl(session)
    user = User(telegram_id=TelegramId(1), role=UserRole.CLIENT)

    with pytest.raises(SaverError):
        await user_saver.save(user)
