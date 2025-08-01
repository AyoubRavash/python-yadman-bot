from aiogram.fsm.state import State, StatesGroup


class AddTaskState(StatesGroup):
    title = State()
    description = State()
    start_date = State()
    end_date = State()
