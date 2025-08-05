from aiogram import types, Router
from aiogram.filters import Command
from psycopg2.errors import UniqueViolation

from keyboards.common import get_main_menu_keyboard
from services.user import insert_user
from models.user import User

router = Router(name='common')


@router.message(Command('start'))
async def cmd_start(msg: types.Message):
    await msg.answer('سلام. به یادمان خوش آمدید 👋 در حال احراز هویت  شما...', reply_markup=get_main_menu_keyboard())
    user = User(
        msg.from_user.id,
        msg.from_user.first_name or "",
        msg.from_user.last_name or "",
        msg.from_user.username or ""
    )
    try:
        await insert_user(user)
    except UniqueViolation:
        await msg.answer('شما با موفقیت وارد شدید 🎉')
        return
    except Exception:
        await msg.answer('ثبت نام با خطا مواجه شد❗ لطفا در بخش حساب کاربری، نسبت به ثبت نام خود اقدام کنید.')
        return
    await msg.answer('ثبت نام با موفقیت انجام شد 🎉')


@router.message(Command('help'))
async def cmd_help(msg: types.Message):
    await msg.answer('به زودی...')
