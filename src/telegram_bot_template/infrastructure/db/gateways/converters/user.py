from adaptix import P
from adaptix.conversion import coercer, get_converter, link

from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.domain.value_objects.user_id import UserId
from telegram_bot_template.infrastructure.db.models.user import (
    UserModel,
)

convert_to_model = get_converter(
    User,
    UserModel,
    recipe=(
        link(
            P[User].id,
            P[UserModel].user_id,
            coercer=lambda vo: vo.to_raw() if vo is not None else None,
        ),
        coercer(
            P[User].telegram_id,
            P[UserModel].telegram_id,
            lambda vo: vo.to_raw(),
        ),
    ),
)

convert_to_domain_entity = get_converter(
    UserModel,
    User,
    recipe=(
        link(
            P[UserModel].user_id,
            P[User].id,
            coercer=lambda value: UserId(value),
        ),
        coercer(
            P[UserModel].telegram_id,
            P[User].telegram_id,
            lambda value: TelegramId(value),
        ),
    ),
)
