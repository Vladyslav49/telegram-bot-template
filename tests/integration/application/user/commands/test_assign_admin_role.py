import pytest
from dishka import AsyncContainer

from telegram_bot_template.application.common.db.user import UserReader
from telegram_bot_template.application.user.commands.assign_admin_role import (
    AssignAdminRole,
    AssignAdminRoleInputDTO,
)
from telegram_bot_template.application.user.commands.create_user import (
    CreateUser,
    CreateUserInputDTO,
)
from telegram_bot_template.application.user.exceptions import (
    UserAlreadyHasAdminRoleError,
    UserIsNotExistsError,
)
from telegram_bot_template.domain.enums.user import UserRole
from telegram_bot_template.domain.exceptions.access import AccessDenied
from telegram_bot_template.domain.value_objects.user_id import UserId


async def test_assign_admin_role_access_denied(
    container: AsyncContainer, user_id: UserId
) -> None:
    assign_admin_role = await container.get(AssignAdminRole)

    with pytest.raises(AccessDenied):
        await assign_admin_role(
            AssignAdminRoleInputDTO(user_id=user_id.to_raw()),
        )


@pytest.mark.usefixtures("make_user_admin")
async def test_assign_admin_role_already_admin(
    container: AsyncContainer, user_id: UserId
) -> None:
    assign_admin_role = await container.get(AssignAdminRole)

    with pytest.raises(UserAlreadyHasAdminRoleError):
        await assign_admin_role(
            AssignAdminRoleInputDTO(user_id=user_id.to_raw()),
        )


@pytest.mark.usefixtures("make_user_admin")
async def test_assign_admin_role_user_not_exists(
    container: AsyncContainer,
) -> None:
    assign_admin_role = await container.get(AssignAdminRole)

    with pytest.raises(UserIsNotExistsError):
        await assign_admin_role(
            AssignAdminRoleInputDTO(user_id=123),
        )


@pytest.mark.usefixtures("make_user_admin")
async def test_assign_admin_role(
    container: AsyncContainer, telegram_id: int
) -> None:
    create_user = await container.get(CreateUser)
    assign_admin_role = await container.get(AssignAdminRole)
    user_reader = await container.get(UserReader)  # type: ignore[type-abstract]

    user_id = await create_user(
        CreateUserInputDTO(telegram_id=telegram_id + 1),
    )
    await assign_admin_role(
        AssignAdminRoleInputDTO(user_id=user_id.to_raw()),
    )
    user = await user_reader.get_by_id(user_id)

    assert user.role is UserRole.ADMINISTRATOR
