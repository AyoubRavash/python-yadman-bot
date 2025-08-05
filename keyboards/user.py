from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_account_action_keyboard(has_account: bool) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text='ویرایش ✏️', callback_data='account_edit') if has_account ==
         True else InlineKeyboardButton(text='ثبت نام ✏️', callback_data='account_add')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)


def get_account_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text='💠 نام', callback_data='edit_account_firstname'), InlineKeyboardButton(
            text='💠 نام خانوادگی', callback_data='edit_account_lastname')],
        [InlineKeyboardButton(
            text='📅 تاریخ تولد', callback_data='edit_account_birthday')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard, resize_keyboard=True)
