import jdatetime
from datetime import datetime


def convert_date(jalali_str: str) -> datetime:
    try:
        # Split by "-"
        if '-' not in jalali_str:
            raise ValueError("Date format must include '-'")

        date_part, time_part = jalali_str.split('-')
        date_part = date_part.strip()
        time_part = time_part.strip()

        # Persian month mapping
        persian_months = {
            'فروردین': 1, 'اردیبهشت': 2, 'خرداد': 3, 'تیر': 4,
            'مرداد': 5, 'شهریور': 6, 'مهر': 7, 'آبان': 8,
            'آذر': 9, 'دی': 10, 'بهمن': 11, 'اسفند': 12
        }

        # Parse date
        day, month_name, year = date_part.split()
        day = int(day)
        month = persian_months.get(month_name)
        if month is None:
            raise ValueError("Invalid Persian month name")
        year = int(year)

        # Parse time
        time_parts = time_part.split(':')
        if len(time_parts) != 3:
            raise ValueError("Time must be in HH:MM:SS format")
        hour, minute, second = map(int, time_parts)

        # Construct and convert
        jdt = jdatetime.datetime(year, month, day, hour, minute, second)
        return jdt.togregorian()

    except Exception as e:
        raise ValueError(f"Invalid date format: {e}")
