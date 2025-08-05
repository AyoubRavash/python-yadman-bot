from utils.convert_date import convert_datetime_to_jalali
from datetime import datetime


def get_task_text(title: str, description: str, start_date: str, end_date: str) -> str:
    return (
        f"📍نام: {title}\n"
        f"💬 توضیحات: {description}\n"
        f"🕒 شروع : {start_date}\n"
        f"⌛ پایان: {end_date}\n"
    )


def get_tasks_text(tasks: list, page: int, total_pages: int) -> str:
    lines = [f'صفحه {page} از {total_pages}:\n']
    for t in tasks:
        start_date = convert_datetime_to_jalali(t['start_date'])
        end_date = convert_datetime_to_jalali(t['end_date'])
        task_status = 'انجام شده ✅' if t['is_done'] else 'انجام نشده ❌'
        t_text = get_task_text(
            t['title'], t['description'], start_date, end_date)
        lines.append(
            f'\n🆔 وظیفه شماره {t['id']}\n\n{t_text}💠 وضعیت: {task_status}',
        )
    return '\n'.join(lines)
