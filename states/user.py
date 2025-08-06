from aiogram.fsm.state import State, StatesGroup


class EditAccountState(StatesGroup):
    field_name = State()
    field_value = State()