from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
import tomlkit
from _pytest.monkeypatch import MonkeyPatch
from _pytest.tmpdir import TempPathFactory
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from dishka import AsyncContainer, Provider, Scope
from dishka.async_container import AsyncContextWrapper, make_async_container
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from testcontainers.postgres import PostgresContainer

from telegram_bot_template.application.common.db.user import (
    UserReader,
    UserSaver,
)
from telegram_bot_template.application.common.id_provider import IdProvider
from telegram_bot_template.application.common.uow import UnitOfWork
from telegram_bot_template.application.user.commands.create_user import (
    CreateUser,
    CreateUserInputDTO,
)
from telegram_bot_template.domain.services.user import UserService
from telegram_bot_template.domain.value_objects.user_id import UserId
from telegram_bot_template.entry_points.config_loader import (
    load_database_config,
)
from telegram_bot_template.entry_points.di import (
    get_command_provider,
    get_database_provider,
    get_gateway_provider,
    get_query_provider,
    get_service_provider,
    get_unit_of_work_provider,
)
from telegram_bot_template.infrastructure.auth.id_provider import RawIdProvider
from telegram_bot_template.infrastructure.db.config import (
    DatabaseConfig,
)


@pytest.fixture(scope="package")
def connection_url() -> Iterator[str]:
    with PostgresContainer(
        image="postgres:16.2-alpine", driver="psycopg"
    ) as postgres:
        yield postgres.get_connection_url()


@pytest.fixture(scope="package")
def config_path(tmp_path_factory: TempPathFactory) -> Path:
    config_data = {
        "database": {
            "pool_size": 1,
        },
    }

    config_path = tmp_path_factory.mktemp("tmp") / "config.toml"
    config_path.write_text(tomlkit.dumps(config_data))

    return config_path


@pytest.fixture(scope="package")
def alembic_config() -> AlembicConfig:
    return AlembicConfig("alembic.ini")


@pytest.fixture()
async def container(
    config_path: Path,
    connection_url: str,
    alembic_config: AlembicConfig,
    monkeypatch: MonkeyPatch,
) -> AsyncIterator[AsyncContainer]:
    monkeypatch.setenv("CONFIG_PATH", str(config_path))
    monkeypatch.setenv("DATABASE_DSN", connection_url)
    monkeypatch.setenv("JWT_KEY", "key")

    async with AsyncContextWrapper(
        make_async_container(
            get_database_provider(),
            get_unit_of_work_provider(),
            get_gateway_provider(),
            get_service_provider(),
            get_command_provider(),
            get_query_provider(),
            get_telegram_provider(),
            context={DatabaseConfig: load_database_config()},
        )
    ) as container:
        engine = await container.get(AsyncEngine)

        async with engine.begin() as connection:
            await connection.run_sync(_run_upgrade, config=alembic_config)

        async with container() as sub_container:
            yield sub_container

        async with engine.begin() as connection:
            await connection.run_sync(_run_downgrade, config=alembic_config)


def get_telegram_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(lambda: RawIdProvider(UserId(1)), provides=IdProvider)
    return provider


def _run_upgrade(connection: Connection, config: AlembicConfig) -> None:
    config.attributes["connection"] = connection
    upgrade(config, "head")


def _run_downgrade(connection: Connection, config: AlembicConfig) -> None:
    config.attributes["connection"] = connection
    downgrade(config, "base")


@pytest.fixture(scope="package")
def telegram_id() -> int:
    return 1111111111


@pytest.fixture()
async def user_id(container: AsyncContainer, telegram_id: int) -> UserId:
    create_user = await container.get(CreateUser)
    return await create_user(
        CreateUserInputDTO(telegram_id=telegram_id),
    )


@pytest.fixture()  # noqa: vulture
async def make_user_admin(container: AsyncContainer, user_id: UserId) -> None:  # noqa: PT004
    uow = await container.get(UnitOfWork)  # type: ignore[type-abstract]
    user_reader = await container.get(UserReader)  # type: ignore[type-abstract]
    user_service = await container.get(UserService)
    user_saver = await container.get(UserSaver)  # type: ignore[type-abstract]

    async with uow:
        user = await user_reader.acquire_by_id(user_id)
        user_service.assign_admin_role(user)
        await user_saver.save(user)
        await uow.commit()
