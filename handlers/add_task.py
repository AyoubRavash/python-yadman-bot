from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from states.task import AddTaskState
from keyboards.task import get_confirm_add_task_keyboard
from services.task import insert_task_db
from services.user import get_user_db
from models.task import Task
from utils.convert_date import convert_date_to_global, convert_datetime_to_jalali
from utils.task import get_task_text
from utils.const_values import error_message

router = Router(name='add_task')


@router.message(lambda msg: msg.text == 'افزودن وظیفه 📝')
async def add_task(msg: types.Message, state: FSMContext):
    user_id = await get_user_db(msg.from_user.id)
    if user_id is None:
        await msg.answer('شما حساب کاربری ندارید. لطفا در بخش حساب کاربری، نسبت به ثبت نام خود اقدام کنید.')
        return

    await state.update_data(user_id=user_id)

    await msg.answer('نام وظیفه را وارد کنید:')
    await state.set_state(AddTaskState.title)


@router.message(AddTaskState.title)
async def handle_title(msg: types.Message, state: FSMContext):

    await state.update_data(title=msg.text)
    await msg.reply('توضیحات وظیفه را وارد کنید:')
    await state.set_state(AddTaskState.description)


@router.message(AddTaskState.description)
async def handle_description(msg: types.Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.reply('تاریخ شروع وظیفه را وارد کنید: مثل 1 فروردین 1400-16:51:00')
    await state.set_state(AddTaskState.start_date)


@router.message(AddTaskState.start_date)
async def handle_start_date(msg: types.Message, state: FSMContext):
    try:
        start_date = convert_date_to_global(msg.text)

        await state.update_data(start_date=start_date)
        await msg.reply('تاریخ پایان وظیفه را وارد کنید: مثل 1 فروردین 1400-16:51:00')
        await state.set_state(AddTaskState.end_date)
    except ValueError:
        await msg.reply('فرمت تاریخ اشتباه است ❌ لطفا به صورت: 1 فروردین 1400-12:00:00 وارد کنید')


@router.message(AddTaskState.end_date)
async def handle_end_date(msg: types.Message, state: FSMContext):
    try:
        end_date = convert_date_to_global(msg.text)
        await state.update_data(end_date=end_date)
        data = await state.get_data()

        start_date = convert_datetime_to_jalali(data['start_date'])
        end_date = convert_datetime_to_jalali(data['end_date'])

        task_text = get_task_text(
            data['title'], data['description'], start_date, end_date)

        await msg.answer(
            "📝 <b>بررسی وظیفه:</b>\n\n" +
            task_text +
            '\nتایید و افزودن وظیفه 👇',
            reply_markup=get_confirm_add_task_keyboard(),
            parse_mode='HTML'
        )

    except ValueError:
        await msg.reply('فرمت تاریخ اشتباه است ❌ لطفا به صورت: 1 فروردین 1400-12:00:00 وارد کنید')


@router.callback_query(lambda c: c.data in ['confirm_task', 'cancel_task'])
async def handle_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirm_task':
        data = await state.get_data()
        task = Task(title=data['title'], description=data['description'],
                    start_date=data['start_date'], end_date=data['end_date'], user_id=data['user_id'])

        result = await insert_task_db(task)
        if result is None:
            await callback_query.answer(error_message, show_alert=True)
            return

        await state.clear()
        await callback_query.answer('وظیفه با موفقیت افزوده شد.', show_alert=True)
    else:
        await state.clear()
        await callback_query.answer('افزودن وظیفه لغو شد.', show_alert=True)
