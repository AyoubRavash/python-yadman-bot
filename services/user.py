from models.user import User
from psycopg2 import connect
from psycopg2.errors import UniqueViolation

from config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASS


async def insert_user(data: User) -> int:
    try:
        with connect(
            host=DB_HOST, database=DB_NAME,
            port=DB_PORT, user=DB_USER, password=DB_PASS
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (telegram_id, first_name, last_name, username, joined_at, birth_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (data.telegram_id, data.first_name, data.last_name,
                     data.username, data.joined_at, data.birth_date)
                )
                result = cur.fetchone()
            conn.commit()
            return result[0]

    except UniqueViolation:
        # This will be raised if telegram_id already exists
        raise  # Re-raise to be caught in caller or handled elsewhere

    except Exception as e:
        print("Unexpected error:", e)
        raise  # Or handle differently


async def get_user(telegram_id: int) -> int | None:
    try:
        with connect(host=DB_HOST, database=DB_NAME, port=DB_PORT, user=DB_USER, password=DB_PASS) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id FROM users WHERE telegram_id = %s
                    """,
                    (telegram_id,)
                )
                result = cur.fetchone()
            conn.commit()
            return result[0] if result else None

    except Exception as e:
        print(e)
        return None

    finally:
        conn.close()
