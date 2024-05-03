from aiogram.fsm.state import State, StatesGroup


class SettingsStatesGroup(StatesGroup):
    registered = State()
