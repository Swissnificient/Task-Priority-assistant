-- 1. Anonymous sessions
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,

    created_at TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    expires_at TEXT
);


-- 2. Tasks
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    session_id TEXT NOT NULL,

    title TEXT NOT NULL,

    description TEXT DEFAULT '',

    priority TEXT NOT NULL DEFAULT 'medium'
        CHECK (
            priority IN ('low', 'medium', 'high')
        ),

    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (
            status IN (
                'pending',
                'in_progress',
                'completed'
            )
        ),

    due_date TEXT,

    created_at TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES sessions(id)
        ON DELETE CASCADE
);


-- 3. Index for retrieving tasks by session
CREATE INDEX IF NOT EXISTS idx_tasks_session_id
ON tasks(session_id);


-- 4. Index for filtering tasks by status
CREATE INDEX IF NOT EXISTS idx_tasks_status
ON tasks(status);


-- 5. Index for sorting tasks by priority
CREATE INDEX IF NOT EXISTS idx_tasks_priority
ON tasks(priority);