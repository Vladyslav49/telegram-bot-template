from aiogram.types import TelegramObject
from dishka import Provider, Scope

from telegram_bot_template.application.common.db.user import (
    UserReader,
    UserSaver,
)
from telegram_bot_template.application.common.uow import UnitOfWork
from telegram_bot_template.application.user.commands.assign_admin_role import (
    AssignAdminRole,
)
from telegram_bot_template.application.user.commands.create_user import (
    CreateUser,
)
from telegram_bot_template.application.user.queries.get_all_telegram_ids import (  # noqa: E501
    GetAllTelegramIds,
)
from telegram_bot_template.application.user.queries.get_current_user import (
    GetCurrentUser,
)
from telegram_bot_template.application.user.queries.get_user_id_by_telegram_id import (  # noqa: E501
    GetUserIdByTelegramId,
)
from telegram_bot_template.domain.services.access import AccessService
from telegram_bot_template.domain.services.user import UserService
from telegram_bot_template.infrastructure.db.config import (
    DatabaseConfig,
)
from telegram_bot_template.infrastructure.db.gateways.user import (
    UserReaderImpl,
    UserSaverImpl,
)
from telegram_bot_template.infrastructure.db.provider import (
    get_engine,
    get_session,
    get_sessionmaker,
)
from telegram_bot_template.infrastructure.db.uow import (
    SQLAlchemyUnitOfWork,
)
from telegram_bot_template.presentation.telegram.provider import (
    get_id_provider,
)


def get_database_provider() -> Provider:
    provider = Provider(scope=Scope.APP)

    provider.from_context(provides=DatabaseConfig, scope=Scope.APP)

    provider.provide(get_engine)
    provider.provide(get_sessionmaker)
    provider.provide(get_session, scope=Scope.REQUEST)

    return provider


def get_unit_of_work_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(SQLAlchemyUnitOfWork, provides=UnitOfWork)
    return provider


def get_gateway_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)

    provider.provide(UserSaverImpl, provides=UserSaver)
    provider.provide(UserReaderImpl, provides=UserReader)

    return provider


def get_service_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide_all(AccessService, UserService)
    return provider


def get_command_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide_all(CreateUser, AssignAdminRole)
    return provider


def get_query_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide_all(
        GetCurrentUser, GetUserIdByTelegramId, GetAllTelegramIds
    )
    return provider


def get_telegram_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)

    provider.from_context(provides=TelegramObject, scope=Scope.REQUEST)

    provider.provide(get_id_provider)

    return provider
