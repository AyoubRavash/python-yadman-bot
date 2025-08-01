from datetime import datetime


class User:
    def __init__(self, telegram_id: int, first_name: str, last_name: str, username: str):
        self.telegram_id = telegram_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.joined_at = datetime.now()
        self.birth_date = None
