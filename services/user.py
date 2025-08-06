from models.user import User
from psycopg2 import connect
from psycopg2.errors import UniqueViolation
from datetime import datetime

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


async def get_user_db(telegram_id: int) -> User | None:
    try:
        with connect(host=DB_HOST, database=DB_NAME, port=DB_PORT, user=DB_USER, password=DB_PASS) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT * FROM users WHERE telegram_id = %s
                    """,
                    (telegram_id,)
                )
                result = cur.fetchone()
                if result[0] is not None:
                    return User(id=result[0], telegram_id=result[1], first_name=result[2], last_name=result[3], username=result[4], birth_date=result[5], joined_at=result[6])
                else:
                    return None
            conn.commit()
            return result[0] if result else None

    except Exception as e:
        print(e)
        return None

    finally:
        conn.close()


async def update_user_field(telegram_id: int, field: str, value: str) -> bool:
    if field == 'firstname':
        db_field = 'first_name'
    elif field == 'lastname':
        db_field = 'last_name'
    elif field == 'birthdate':
        db_field = 'birth_date'
    else:
        return False

    try:
        with connect(host=DB_HOST, database=DB_NAME, port=DB_PORT, user=DB_USER, password=DB_PASS) as conn:
            with conn.cursor() as cur:
                query = f"UPDATE users SET {db_field} = %s WHERE telegram_id = %s"
                cur.execute(query, (value, telegram_id))
                conn.commit()
                return cur.rowcount > 0  # True if any row was updated

    except Exception as e:
        print("Error updating user field:", e)
        return False

    finally:
        try:
            conn.close()
        except:
            pass
