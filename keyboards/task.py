from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_confirm_add_task_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text='بله ✅', callback_data='confirm_task'), InlineKeyboardButton(
            text='خیر ❌', callback_data='cancel_task')]
    ]
    return InlineKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
