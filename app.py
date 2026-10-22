from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
# If you don't use cookies/sessions yet, set a dummy session ID for foreign-key validation
DEFAULT_SESSION_ID = "guest_user_1"

def get_db():
    conn = sqlite3.connect('tasks.db')
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    # Sort: pending/in_progress first, then high > medium > low, then due_date
    query = '''
        SELECT * FROM tasks
        ORDER BY
            CASE status
                WHEN 'pending' THEN 1
                WHEN 'in_progress' THEN 2
                WHEN 'completed' THEN 3
                ELSE 4
            END ASC,
            CASE priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                WHEN 'low' THEN 3
                ELSE 4
            END ASC,
            due_date ASC;
    '''
    tasks = conn.execute(query).fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description', '')
    priority = request.form.get('priority', 'medium').lower()
    due_date = request.form.get('due_date') or None

    conn = get_db()
    # Ensure our dummy session exists so the FOREIGN KEY constraint passes
    conn.execute('INSERT OR IGNORE INTO sessions (id) VALUES (?)', (DEFAULT_SESSION_ID,))
    conn.execute(
        '''
        INSERT INTO tasks (session_id, title, description, priority, due_date)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (DEFAULT_SESSION_ID, title, description, priority, due_date)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):
    new_status = request.form.get('status')
    if new_status in ('pending', 'in_progress', 'completed'):
        conn = get_db()
        conn.execute(
            'UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (new_status, id)
        )
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    conn = get_db()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)