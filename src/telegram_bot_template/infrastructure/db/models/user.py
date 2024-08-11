from typing import Final, final

from sqlalchemy import BigInteger, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from telegram_bot_template.domain.enums.user_role import UserRole
from telegram_bot_template.infrastructure.db.models.base import Base

USER_ROLE_ENUM: Final = ENUM(
    UserRole,
    name="user_role",
    create_type=False,
    create_constraint=True,
    validate_strings=True,
)

UNIQUE_USER_TELEGRAM_ID_CONSTRAINT_NAME: Final = "uq_user_telegram_id"


@final
class UserModel(Base):
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    role: Mapped[UserRole] = mapped_column(USER_ROLE_ENUM)

    __table_args__ = (
        UniqueConstraint(
            "telegram_id", name=UNIQUE_USER_TELEGRAM_ID_CONSTRAINT_NAME
        ),
    )
