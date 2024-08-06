from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from telegram_bot_template.infrastructure.db.config import (
    DatabaseConfig,
)


async def get_engine(
    database_config: DatabaseConfig,
) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(
        database_config.dsn, pool_size=database_config.pool_size
    )
    yield engine
    await engine.dispose()


def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine)


async def get_session(
    sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with sessionmaker() as session:
        yield session
