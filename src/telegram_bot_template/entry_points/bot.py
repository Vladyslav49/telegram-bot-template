import logging.config
from datetime import timedelta
from functools import partial
from pathlib import Path
from typing import Final

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_broadcaster import Broadcaster, DefaultMailerSettings
from aiogram_broadcaster.storages.redis import RedisMailerStorage
from aiogram_dialog import setup_dialogs
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentCompileCore
from aiogram_i18n.managers import ConstManager
from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import setup_dishka

from telegram_bot_template.entry_points.config_loader import (
    load_database_config,
    load_logging_config,
    load_redis_config,
    load_telegram_config,
)
from telegram_bot_template.entry_points.di import (
    get_command_provider,
    get_database_provider,
    get_factory_provider,
    get_gateway_provider,
    get_query_provider,
    get_service_provider,
    get_telegram_provider,
    get_unit_of_work_provider,
)
from telegram_bot_template.infrastructure.db.config import (
    DatabaseConfig,
)
from telegram_bot_template.presentation.telegram.broadcast.router import (
    ROUTER as BROADCASTER_ROUTER,
)
from telegram_bot_template.presentation.telegram.start.dialog import (
    DIALOG as START_DIALOG,
)
from telegram_bot_template.presentation.telegram.start.router import (
    ROUTER as START_ROUTER,
)
from telegram_bot_template.presentation.telegram.widgets.i18n import (
    I18N_CONTEXT_KEY,
)

DEFAULT_LOCALE: Final = "en"

MAILER_INTERVAL: Final = 0.05


def get_dispatcher() -> Dispatcher:
    container = make_async_container(
        get_database_provider(),
        get_unit_of_work_provider(),
        get_gateway_provider(),
        get_service_provider(),
        get_factory_provider(),
        get_command_provider(),
        get_query_provider(),
        get_telegram_provider(),
        context={DatabaseConfig: load_database_config()},
    )

    redis_config = load_redis_config()

    storage = RedisStorage.from_url(
        redis_config.dsn,
        key_builder=DefaultKeyBuilder(with_destiny=True),
        state_ttl=timedelta(days=1),
        data_ttl=timedelta(days=1),
    )

    dp = Dispatcher(
        storage=storage, events_isolation=storage.create_isolation()
    )

    i18n_middleware = I18nMiddleware(
        FluentCompileCore(
            Path(__file__).parent.parent
            / "presentation"
            / "telegram"
            / "locales"
            / "{locale}",
            default_locale=DEFAULT_LOCALE,
        ),
        manager=ConstManager(),
        context_key=I18N_CONTEXT_KEY,
    )
    i18n_middleware.setup(dp)

    dp.message.outer_middleware.register(i18n_middleware)
    dp.callback_query.outer_middleware.register(i18n_middleware)

    broadcaster = Broadcaster(
        storage=RedisMailerStorage.from_url(redis_config.dsn),
        default=DefaultMailerSettings(
            interval=MAILER_INTERVAL,
            handle_retry_after=True,
            destroy_on_complete=True,
            run_on_startup=True,
        ),
    )
    broadcaster.setup(dp)

    setup_dishka(container, dp, auto_inject=True)

    setup_dialogs(dp)

    dp.include_routers(START_ROUTER, BROADCASTER_ROUTER)

    dp.include_router(START_DIALOG)

    dp.shutdown.register(partial(close_container, container))

    return dp


async def close_container(container: AsyncContainer) -> None:
    await container.close()


def main() -> None:
    bot = Bot(
        load_telegram_config().bot_api_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    get_dispatcher().run_polling(bot)


if __name__ == "__main__":
    logging.config.dictConfig(load_logging_config().config)
    main()
