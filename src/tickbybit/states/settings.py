from aiogram.fsm.state import State, StatesGroup


class SettingsStatesGroup(StatesGroup):
    registered = State()

class SStatesGroup(StatesGroup):
    start = State()
    input_format_value = State()
    triggers = State()
