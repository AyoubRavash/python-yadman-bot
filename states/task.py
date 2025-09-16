from aiogram.fsm.state import State, StatesGroup


class AddTaskState(StatesGroup):
    title = State()
    description = State()
    start_date = State()
    end_date = State()
    user_id = State()

class GetTaskState(StatesGroup):
    id = State()

class EditTaskState(StatesGroup):
    field_name = State()
    field_value = State()