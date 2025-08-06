from aiogram import types, Router
from aiogram.filters import Command
from psycopg2.errors import UniqueViolation
from aiogram.fsm.context import FSMContext

from services.user import get_user_db, insert_user, update_user_field
from states.user import EditAccountState
from models.user import User
from keyboards.user import get_account_action_keyboard, get_account_keyboard
from utils.user import get_user_text
from utils.const_values import error_message
from utils.convert_date import convert_date_to_global

router = Router(name='add_task')


@router.message(lambda msg: msg.text == 'حساب کاربری 👤')
@router.message(Command('account'))
async def cmd_account(msg: types.Message):
    user = await get_user_db(msg.from_user.id)
    if user is None:
        await msg.answer('شما حساب کاربری ندارید ‼️', reply_markup=get_account_action_keyboard(False))
    else:
        await msg.answer(get_user_text(user), reply_markup=get_account_action_keyboard(True))


@router.callback_query(lambda c: c.data and c.data.startswith('account_'))
async def handler_account(callback_query: types.CallbackQuery):
    action = callback_query.data.split('_')[1]
    if action == 'add':
        user = User(
            callback_query.message.from_user.id,
            callback_query.message.from_user.first_name or "",
            callback_query.message.from_user.last_name or "",
            callback_query.message.from_user.username or "",
        )
        try:
            await insert_user(user)
        except UniqueViolation:
            await callback_query.message.answer('شما با موفقیت وارد شدید 🎉')
            return
        except Exception:
            await callback_query.message.answer(error_message, show_alert=True)
            return
        await callback_query.message.answer('ثبت نام با موفقیت انجام شد 🎉')
    else:
        await callback_query.message.edit_text('یکی از گزینه های زیر را انتخاب کنید 👇', reply_markup=get_account_keyboard())


@router.callback_query(lambda c: c.data and c.data.startswith('edit_account_'))
async def handler_account_action(callback_query: types.CallbackQuery, state: FSMContext):
    field = callback_query.data.split('_')[2]
    if field == 'firstname':
        lang_field = 'نام'
    elif field == 'lastname':
        lang_field = 'نام خانوادگی'
    elif field == 'birthdate':
        lang_field = 'تاریخ تولد'
    else:
        await callback_query.message.answer(error_message, show_alert=True)

    await callback_query.message.edit_text(f'{lang_field} جدید را وارد کنید:')
    await state.update_data(field_name=field)
    await state.set_state(EditAccountState.field_value)


@router.message(EditAccountState.field_value)
async def handler_edit_account(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    field_value = msg.text
    if data['field_name'] == 'birthdate':
        try:
            field_value = convert_date_to_global(field_value)
        except:
            await msg.answer('تاریخ تولد خود را طبق فرمت 16 مرداد 1387 وارد کنید', show_alert=True)

    result = await update_user_field(msg.from_user.id, data['field_name'], field_value)
    if result:
        text = 'حساب کاربری شما با موفقیت ویرایش شد 🎉'
        await state.clear()
    else:
        text = error_message
    await msg.answer(text, show_alert=True)
