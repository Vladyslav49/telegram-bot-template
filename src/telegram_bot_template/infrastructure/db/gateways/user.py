from typing import final, override

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from telegram_bot_template.application.common.db.user import (
    UserReader,
    UserSaver,
)
from telegram_bot_template.application.common.exceptions import SaverError
from telegram_bot_template.application.user.exceptions import (
    UserIsNotExistsError,
    UserTelegramIdAlreadyExistsError,
)
from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.domain.value_objects.user_id import UserId
from telegram_bot_template.infrastructure.db.gateways.converters.user import (
    convert_to_domain_entity,
    convert_to_model,
)
from telegram_bot_template.infrastructure.db.models.user import (
    UNIQUE_USER_TELEGRAM_ID_CONSTRAINT_NAME,
    UserModel,
)


@final
class UserSaverImpl(UserSaver):
    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession, /) -> None:  # noqa: vulture
        self._session = session

    @override
    async def save(self, user: User, /) -> UserId:
        model = convert_to_model(user)
        model = await self._session.merge(model)

        try:
            await self._session.flush((model,))
        except IntegrityError as e:
            if (
                e.orig.diag.constraint_name  # type: ignore[union-attr]
                == UNIQUE_USER_TELEGRAM_ID_CONSTRAINT_NAME
            ):
                raise UserTelegramIdAlreadyExistsError from e
            raise SaverError from e

        return UserId(model.user_id)


@final
class UserReaderImpl(UserReader):
    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession, /) -> None:  # noqa: vulture
        self._session = session

    @override
    async def get_by_id(self, id: UserId, /) -> User:
        stmt = select(UserModel).where(UserModel.user_id == id.to_raw())
        result = await self._session.execute(stmt)
        try:
            model = result.scalar_one()
        except NoResultFound as e:
            raise UserIsNotExistsError from e
        return convert_to_domain_entity(model)

    @override
    async def acquire_by_id(self, id: UserId, /) -> User:
        stmt = (
            select(UserModel)
            .with_for_update()
            .where(UserModel.user_id == id.to_raw())
        )
        result = await self._session.execute(stmt)
        try:
            model = result.scalar_one()
        except NoResultFound as e:
            raise UserIsNotExistsError from e
        return convert_to_domain_entity(model)

    @override
    async def get_id_by_telegram_id(
        self, telegram_id: TelegramId, /
    ) -> UserId:
        stmt = select(UserModel.user_id).where(
            UserModel.telegram_id == telegram_id.to_raw()
        )
        result = await self._session.execute(stmt)
        try:
            user_id = result.scalar_one()
        except NoResultFound as e:
            raise UserIsNotExistsError from e
        return UserId(user_id)

    @override
    async def get_all_telegram_ids(self) -> tuple[TelegramId, ...]:
        stmt = select(UserModel.telegram_id)
        result = await self._session.scalars(stmt)
        return tuple(TelegramId(telegram_id) for telegram_id in result.all())
