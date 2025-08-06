from utils.convert_date import convert_datetime_to_jalali
from models.user import User


def get_user_text(user: User) -> str:
    joined_date = 'وجود ندارد'
    birth_date = 'وجود ندارد'

    if user.joined_at is not None:
        joined_date = convert_datetime_to_jalali(user.joined_at)

    if user.birth_date is not None:
        birth_date = convert_datetime_to_jalali(user.birth_date)

    return (
        f"💠 نام: {user.first_name}\n"
        f"💠 نام خانوادگی: {user.last_name}\n"
        f"👤 نام کاربری : {user.username}\n"
        f"📅 تاریخ عضویت: {joined_date}\n"
        f"📅 تاریخ تولد: {birth_date}\n"
    )
