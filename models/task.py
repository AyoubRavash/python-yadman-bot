from datetime import datetime

class Task:
    def __init__(self, title: str, description: str, start_date: datetime, end_date: datetime, user_id: int):
        self.title = title.strip()
        self.description = description.strip()
        self.start_date = start_date
        self.end_date = end_date
        self.is_done = False
        self.user_id = user_id
