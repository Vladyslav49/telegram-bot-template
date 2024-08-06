from contextlib import suppress

from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.domain.value_objects.user_id import UserId
from telegram_bot_template.infrastructure.db.models.user import (
    UserModel,
)


def convert_to_model(entity: User) -> UserModel:
    model = UserModel(
        telegram_id=entity.telegram_id.to_raw(), role=entity.role
    )
    with suppress(AttributeError):  # set user_id if entity has id attribute
        model.user_id = entity.id.to_raw()
    return model


def convert_to_domain_entity(model: UserModel) -> User:
    entity = User(telegram_id=TelegramId(model.telegram_id), role=model.role)
    entity.id = UserId(model.user_id)
    return entity
