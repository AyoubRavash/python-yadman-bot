from psycopg2 import connect
from config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASS
from models.task import Task


async def insert_task(data: Task) -> int | None:
    try:
        with connect(host=DB_HOST, database=DB_NAME, port=DB_PORT, user=DB_USER, password=DB_PASS) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO tasks (title, description, start_date, end_date, is_done, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (data.title, data.description,
                     data.start_date, data.end_date, data.is_done, data.user_id)
                )
                result = cur.fetchone()
            conn.commit()
            return result[0] if result else None

    except Exception as e:
        print(e)
        return None

    finally:
        conn.close()
