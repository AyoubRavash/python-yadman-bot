from datetime import datetime
from utils.convert_date import convert_date


class Task:
    def __init__(self, title: str, description: str, start_date: datetime, end_date: datetime):
        self.title = title.strip()
        self.description = description.strip()
        self.start_date = convert_date(start_date)
        self.end_date = convert_date(end_date)
        self.is_done = False
