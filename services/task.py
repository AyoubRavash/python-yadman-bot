from psycopg2 import connect
from math import ceil

from config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASS
from models.task import Task
from utils.const_values import limit


async def insert_task_db(data: Task) -> int | None:
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


async def get_tasks_db(user_id: int, page: int = 1) -> tuple[list, int] | None:
    try:
        with connect(host=DB_HOST, database=DB_NAME, port=DB_PORT, user=DB_USER, password=DB_PASS) as conn:
            with conn.cursor() as cur:
                # شمارش کل تسک‌ها
                cur.execute(
                    "SELECT COUNT(*) FROM tasks WHERE user_id = %s",
                    (user_id,)
                )
                total_count = cur.fetchone()[0]

                # دریافت تسک‌ها بر اساس end_date صعودی
                cur.execute(
                    """
                    SELECT id, title, description, start_date, end_date, is_done
                    FROM tasks
                    WHERE user_id = %s
                    ORDER BY end_date ASC
                    LIMIT %s OFFSET %s
                    """,
                    (user_id, limit, (page - 1) * limit)
                )
                rows = cur.fetchall()

                # تبدیل به دیکشنری
                tasks = []
                for row in rows:
                    task = {
                        'id': row[0],
                        'title': row[1],
                        'description': row[2],
                        'start_date': row[3],
                        'end_date': row[4],
                        'is_done': row[5],
                    }
                    tasks.append(task)

            total_pages = ceil(total_count / limit) if total_count else 1
            return tasks, total_pages

    except Exception as e:
        print(e)
        return None
    finally:
        conn.close()
