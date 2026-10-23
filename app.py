"""Simple local classroom demo: one shared task list."""
from contextlib import contextmanager
from datetime import date
from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
SESSION_ID = "guest_user_1"
PRIORITIES = {"high": 0, "medium": 1, "low": 2}
STATUSES = {"pending": 0, "in_progress": 1, "completed": 2}


@contextmanager
def database():
    """Open a connection, commit successful work, and always close it."""
    connection = sqlite3.connect(BASE_DIR / "tasks.db")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()


# Create tables and the shared session required by schema.sql.
with database() as connection:
    connection.executescript((BASE_DIR / "schema.sql").read_text())
    connection.execute("INSERT OR IGNORE INTO sessions (id) VALUES (?)", (SESSION_ID,))


def task_order(task):
    return (STATUSES[task["status"]], PRIORITIES[task["priority"]],
            not bool(task["due_date"]), task["due_date"] or "")


@app.get("/")
def index():
    with database() as connection:
        tasks = connection.execute(
            "SELECT * FROM tasks WHERE session_id = ? ORDER BY id", (SESSION_ID,)
        ).fetchall()
    return render_template("index.html", tasks=sorted(tasks, key=task_order))


@app.post("/add")
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "medium").strip().lower()
    due_date = request.form.get("due_date", "").strip()

    if not title or len(title) > 200:
        return "Title must contain 1–200 characters. Go back and try again.", 400
    if priority not in PRIORITIES:
        return "Choose high, medium, or low. Go back and try again.", 400
    if due_date:
        try:
            if date.fromisoformat(due_date).isoformat() != due_date:
                return "Use YYYY-MM-DD for the date. Go back and try again.", 400
        except ValueError:
            return "Invalid date. Go back and try again.", 400

    with database() as connection:
        connection.execute(
            """INSERT INTO tasks (session_id, title, description, priority, due_date)
               VALUES (?, ?, ?, ?, ?)""",
            (SESSION_ID, title, description, priority, due_date or None))
    return redirect(url_for("index"), code=303)


@app.post("/update-status/<int:id>")
def update_status(id):
    status = request.form.get("status", "")
    if status not in STATUSES:
        return "Invalid status. Go back and try again.", 400
    with database() as connection:
        result = connection.execute(
            """UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP
               WHERE id = ? AND session_id = ?""", (status, id, SESSION_ID))
    if result.rowcount == 0:
        return "Task not found.", 404
    return redirect(url_for("index"), code=303)


@app.post("/delete/<int:id>")
def delete_task(id):
    with database() as connection:
        result = connection.execute(
            "DELETE FROM tasks WHERE id = ? AND session_id = ?", (id, SESSION_ID))
    if result.rowcount == 0:
        return "Task not found.", 404
    return redirect(url_for("index"), code=303)


if __name__ == "__main__":
    app.run()
