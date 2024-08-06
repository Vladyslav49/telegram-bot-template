from typing import Final

from aiogram_dialog import Dialog, LaunchMode, Window

from telegram_bot_template.presentation.telegram.start.state import StartSG
from telegram_bot_template.presentation.telegram.widgets.i18n import I18NConst

DIALOG: Final = Dialog(
    Window(
        I18NConst("start"),
        state=StartSG.menu,
    ),
    launch_mode=LaunchMode.ROOT,
    name=__name__,
)
