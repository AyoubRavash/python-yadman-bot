from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from services.task import get_tasks_db
from services.user import get_user_db
from utils.const_values import error_message
from utils.task import get_tasks_text
from keyboards.common import get_pagination_keyboard

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
    await msg.answer(text, reply_markup=get_pagination_keyboard(page, total_pages, user_id))


@router.callback_query(lambda c: c.data and c.data.startswith('page_'))
async def paginate_tasks(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    page = int(data[1])
    user_id = int(data[2])

    tasks, total_pages = await get_tasks_db(user_id, page)
    if tasks is None:
        await callback_query.answer(error_message, show_alert=True)
        return

    text = get_tasks_text(tasks, page, total_pages=total_pages)
    await callback_query.message.edit_text(
        text,
        reply_markup=get_pagination_keyboard(page, total_pages, user_id)
    )
