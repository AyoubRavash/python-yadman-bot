from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text='وظایف من 📌')],
        [KeyboardButton(text='افزودن وظیفه 📝'), KeyboardButton(
            text='جست و جو 🔎')],
        [KeyboardButton(text='حساب کاربری 👤'),
         KeyboardButton(text='تیم من 👥')],
        [KeyboardButton(text='راهنما 🗒️')],
        [KeyboardButton(text='سوالات متداول ❓'),
         KeyboardButton(text='ارتباط با پشتیبانی 📞')]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_pagination_keyboard(current_page: int, total_pages: int, user_id: int) -> InlineKeyboardMarkup:
    buttons = []
    if current_page > 1:
        buttons.append(InlineKeyboardButton(text='صفحه قبل ⏪',
                       callback_data=f'page_{current_page-1}_{user_id}'))
    if current_page < total_pages:
        buttons.append(InlineKeyboardButton(text='صفحه بعد ⏩',
                       callback_data=f'page_{current_page+1}_{user_id}'))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
