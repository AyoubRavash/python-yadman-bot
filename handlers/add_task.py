from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.add_task import AddTaskState
from keyboards.task import get_confirm_add_task_keyboard
from services.add_task import insert_task
from models.task import Task

router = Router(name='add_task')


@router.message(lambda msg: msg.text == 'افزودن وظیفه 📝')
async def add_task(msg: types.Message, state: FSMContext):
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
    await state.update_data(start_date=msg.text)
    await msg.reply('تاریخ پایان وظیفه را وارد کنید: مثل 1 فروردین 1400-16:51:00')
    await state.set_state(AddTaskState.end_date)


@router.message(AddTaskState.end_date)
async def handle_end_date(msg: types.Message, state: FSMContext):
    await state.update_data(end_date=msg.text)
    data = await state.get_data()

    task_text = (
        f"📝 <b>بررسی وظیفه:</b>\n"
        f"عنوان 📍: {data['title']}\n"
        f"توضیحات 💬: {data['description']}\n"
        f"شروع 🕒: {data['start_date']}\n"
        f"پایان ⌛: {data['end_date']}"
    )

    await msg.answer(task_text, reply_markup=get_confirm_add_task_keyboard(), parse_mode='HTML')


@router.callback_query(lambda c: c.data in ['confirm_task', 'cancel_task'])
async def handle_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'confirm_task':
        data = await state.get_data()
        task = Task(data['title'], data['description'],
                    data['start_date'], data['end_date'])

        result = await insert_task(task)
        if result is None:
            await callback_query.answer('افزودن وظیفه با خطا مواجه شد.', show_alert=True)
            return

        await state.finish()
        await callback_query.answer('وظیفه با موفقیت افزوده شد.', show_alert=True)
    else:
        await state.finish()
        await callback_query.answer('افزودن وظیفه لغو شد.', show_alert=True)
