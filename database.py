import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "tasks.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

EDITABLE_TASK_FIELDS = {
    "title",
    "description",
    "priority",
    "status",
    "due_date",
    "due_time",
}


@contextmanager
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    with get_connection() as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

        columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(tasks)")
        }
        if "due_time" not in columns:
            connection.execute("ALTER TABLE tasks ADD COLUMN due_time TEXT")


def _format_due_time(value):
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError("due_time must be a string in 12-hour or 24-hour format")

    for time_format in ("%I:%M %p", "%I %p", "%H:%M"):
        try:
            return datetime.strptime(value.strip(), time_format).strftime("%I:%M %p")
        except ValueError:
            continue
    raise ValueError("due_time must be like '2:30 PM' or '14:30'")


def create_task(session_id, title, description="", priority="medium",
                status="pending", due_date=None, due_time=None):
    due_time = _format_due_time(due_time)
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks
                (session_id, title, description, priority, status, due_date, due_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (session_id, title, description, priority, status, due_date, due_time),
        )
        return cursor.lastrowid


def update_task(task_id, session_id, **updates):
    if not updates:
        raise ValueError("At least one task field must be provided")

    invalid_fields = updates.keys() - EDITABLE_TASK_FIELDS
    if invalid_fields:
        raise ValueError(f"Fields cannot be edited: {', '.join(sorted(invalid_fields))}")
    if "due_time" in updates:
        updates["due_time"] = _format_due_time(updates["due_time"])

    assignments = ", ".join(f"{field} = ?" for field in updates)
    values = [*updates.values(), task_id, session_id]
    with get_connection() as connection:
        cursor = connection.execute(
            f"""
            UPDATE tasks
            SET {assignments}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND session_id = ?
            """,
            values,
        )
        return cursor.rowcount > 0


initialize_database()
print("Database created successfully!")