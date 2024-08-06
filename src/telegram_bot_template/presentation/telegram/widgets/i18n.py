from typing import Final, final, override

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_i18n import I18nContext

I18N_CONTEXT_KEY: Final = "i18n"


@final
class I18NConst(Const):
    @override
    async def _render_text(self, data: dict, manager: DialogManager) -> str:  # type: ignore[type-arg]
        i18n: I18nContext = manager.middleware_data[I18N_CONTEXT_KEY]
        return i18n.get(self.text)
