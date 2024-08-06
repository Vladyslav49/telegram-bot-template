from typing import final

from aiogram.fsm.state import State, StatesGroup


@final
class StartSG(StatesGroup):
    menu = State()
