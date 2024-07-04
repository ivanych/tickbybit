from aiogram.fsm.state import State, StatesGroup


class SettingsStatesGroup(StatesGroup):
    registered = State()

class SStatesGroup(StatesGroup):
    start = State()
    value_format = State()
    path_triggers = State()
