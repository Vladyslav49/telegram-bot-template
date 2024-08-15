from telegram_bot_template.domain.entities.user import User
from telegram_bot_template.domain.value_objects.telegram_id import TelegramId
from telegram_bot_template.domain.value_objects.user_id import UserId
from telegram_bot_template.infrastructure.db.models.user import (
    UserModel,
)


def convert_to_model(entity: User) -> UserModel:
    return UserModel(
        user_id=entity.id.to_raw() if entity.id is not None else None,
        telegram_id=entity.telegram_id.to_raw(),
        role=entity.role,
    )


def convert_to_domain_entity(model: UserModel) -> User:
    return User(
        id=UserId(model.user_id),
        telegram_id=TelegramId(model.telegram_id),
        role=model.role,
    )
