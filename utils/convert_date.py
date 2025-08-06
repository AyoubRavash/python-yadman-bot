import jdatetime
from datetime import datetime, date


def convert_date_to_global(jalali_str: str) -> datetime:
    try:
        has_time = '-' in jalali_str
        # Split by "-"
        if has_time:
            date_part, time_part = jalali_str.split('-')
            time_part = time_part.strip()
        else:
            date_part = jalali_str

        date_part = date_part.strip()

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

        if has_time:
            # Parse time
            time_parts = time_part.split(':')
            if len(time_parts) != 3:
                raise ValueError("Time must be in HH:MM:SS format")
            hour, minute, second = map(int, time_parts)

        jdt = jdatetime.datetime(year, month, day, hour, minute,
                                 second) if has_time else jdatetime.date(year, month, day)
        # Construct and convert
        return jdt.togregorian()

    except Exception as e:
        raise ValueError(f"Invalid date format: {e}")


def convert_datetime_to_jalali(gregorian_dt: datetime | date) -> str:
    jdt = jdatetime.datetime.fromgregorian(datetime=gregorian_dt) if type(
        gregorian_dt) == datetime else jdatetime.date.fromgregorian(date=gregorian_dt)
    
    persian_months = [
        '',  # index 0 unused
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر',
        'مرداد', 'شهریور', 'مهر', 'آبان',
        'آذر', 'دی', 'بهمن', 'اسفند'
    ]

    day = jdt.day
    month_name = persian_months[jdt.month]
    year = jdt.year

    result = f"{day} {month_name} {year}"

    if type(gregorian_dt) == datetime:
        time_str = f"{jdt.hour:02d}:{jdt.minute:02d}:{jdt.second:02d}"
        result + f' {time_str}'
    return result
