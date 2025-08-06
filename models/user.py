from datetime import datetime, date


class User:
    def __init__(self, telegram_id: int, first_name: str, last_name: str, username: str, joined_at: datetime = datetime.now(), birth_date: date = None, id: int = None):
        self.id = id
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.joined_at = joined_at
        self.birth_date = birth_date
