from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from services.task import get_tasks_db, get_task_db, delete_task_db
from services.user import get_user_db
from utils.const_values import error_message
from utils.task import get_tasks_text, get_task_text
from keyboards.task import get_tasks_pagination_keyboard, get_task_keyboard
from states.task import GetTaskState
from utils.convert_date import convert_datetime_to_jalali

router = Router(name='tasks')


@router.message(lambda msg: msg.text == 'وظایف من 📌')
async def get_tasks(msg: types.Message):
    user = await get_user_db(msg.from_user.id)
    if user is None:
        await msg.answer('شما حساب کاربری ندارید. لطفا در بخش حساب کاربری، نسبت به ثبت نام خود اقدام کنید.')
        return

    user_id = user.id

    page = 1
    tasks, total_pages = await get_tasks_db(user_id, page)
    if tasks is None:
        await msg.answer(error_message, show_alert=True)
        return

    text = get_tasks_text(tasks, page, total_pages=total_pages)

    await msg.answer(text, reply_markup=get_tasks_pagination_keyboard(page, total_pages, user_id))


@router.callback_query(lambda c: c.data and c.data.startswith('tasks_page'))
async def paginate_tasks(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    page = int(data[2])
    user_id = int(data[3])

    tasks, total_pages = await get_tasks_db(user_id, page)
    if tasks is None:
        await callback_query.answer(error_message, show_alert=True)
        return

    text = get_tasks_text(tasks, page, total_pages=total_pages)

    await callback_query.message.edit_text(
        text,
        reply_markup=get_tasks_pagination_keyboard(
            page, total_pages, user_id)
    )


@router.callback_query(lambda c: c.data and c.data == 'tasks_select')
async def get_task(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('شماره وظیفه را وارد کنید:')
    await state.set_state(GetTaskState.id)


@router.message(GetTaskState.id)
async def get_task_handler(msg: types.Message, state: FSMContext):
    task_id = msg.text
    if (task_id is None or task_id.isdigit() == False):
        await msg.answer('شماره وظیفه نامعتبر است ‼️', show_alert=True)
        return

    task = await get_task_db(task_id)
    if task is None:
        await msg.answer(f'وظیفه با شماره {task_id} یافت نشد.', show_alert=True)
        return

    await state.clear()
    start_date = convert_datetime_to_jalali(task.start_date)
    end_date = convert_datetime_to_jalali(task.end_date)
    await msg.reply(get_task_text(task.title, task.description, start_date, end_date, is_done=task.is_done), reply_markup=get_task_keyboard(task.is_done, task.id))


@router.callback_query(lambda c: c.data and c.data.startswith('task_delete'))
async def delete_task(callback_query: types.CallbackQuery):
    task_id = int(callback_query.data.split('_')[2])
    result = await delete_task_db(task_id)
    if (result == False):
        await callback_query.message.answer(error_message, show_alert=True)
        return

    await callback_query.message.answer('وظیفه با موفقیت حذف شد 🎉', show_alert=True)
