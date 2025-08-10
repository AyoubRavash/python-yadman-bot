from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_confirm_add_task_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text='بله ✅', callback_data='confirm_task'), InlineKeyboardButton(
            text='خیر ❌', callback_data='cancel_task')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def get_tasks_pagination_keyboard(current_page: int, total_pages: int, user_id: int) -> InlineKeyboardMarkup:
    page_buttons = []
    if current_page > 1:
        page_buttons.append(InlineKeyboardButton(text='صفحه قبل ⏪',
                                                 callback_data=f'tasks_page_{current_page-1}_{user_id}'))
    if current_page < total_pages:
        page_buttons.append(InlineKeyboardButton(text='صفحه بعد ⏩',
                                                 callback_data=f'tasks_page_{current_page+1}_{user_id}'))

    return InlineKeyboardMarkup(inline_keyboard=[
        page_buttons,
        [InlineKeyboardButton(
            text='انتخاب یک وظیفه ☝️', callback_data='tasks_select')]
    ])


def get_task_keyboard(current_status: bool) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='حذف ❌', callback_data='task_delete'), InlineKeyboardButton(
            text='ویرایش ✏️', callback_data='task_edit')],
        [InlineKeyboardButton(
            text=f'تغییر وضعیت به {'انجام شده 🙂' if current_status == False else 'انجام نشده ☹️'}', callback_data='task_status')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
