from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text='کار های من 📌')],
        [KeyboardButton(text='افزودن کار 📝'), KeyboardButton(
            text='جست و جوی پیشرفته 🔎')],
        [KeyboardButton(text='حساب کاربری 👤'),
         KeyboardButton(text='تیم من 👥')],
        [KeyboardButton(text='راهنما 🗒️')],
        [KeyboardButton(text='سوالات متداول ❓'),
         KeyboardButton(text='ارتباط با پشتیبانی 📞')]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
