import jdatetime
from datetime import datetime


def convert_date(jalali_str: str) -> datetime:
    import re
    parts = re.split(r'-', jalali_str)
    date_part = parts[0].strip()
    time_part = parts[1].strip() if len(parts) > 1 else '00:00:00'

    persian_months = {
        'فروردین': 1, 'اردیبهشت': 2, 'خرداد': 3, 'تیر': 4,
        'مرداد': 5, 'شهریور': 6, 'مهر': 7, 'آبان': 8,
        'آذر': 9, 'دی': 10, 'بهمن': 11, 'اسفند': 12
    }

    day, month_name, year = date_part.split()
    day = int(day)
    month = persian_months[month_name]
    year = int(year)

    hour, minute, second = map(int, time_part.split(':'))

    jdt = jdatetime.datetime(year, month, day, hour, minute, second)
    gdt = jdt.togregorian()
    return gdt
