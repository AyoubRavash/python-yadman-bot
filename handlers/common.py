from aiogram import types, Router
from aiogram.filters import Command
from keyboards.main_menu import get_main_menu_keyboard

router = Router(name='common')


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('سلام. به یادمان خوش اومدی 👋', reply_markup=get_main_menu_keyboard())
