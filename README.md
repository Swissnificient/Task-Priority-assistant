## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Swissnificient/Task-Priority-assistant.git
cd Task-Priority-assistant
```

### 2. Create a virtual environment

Use Python 3.12:

```bash
python3 -m venv .venv-local
```
### 3. Activate the virtual environment

On Ubuntu/Linux or macOS:

```bash
source .venv-local/bin/activate
```

Your terminal prompt should now begin with `(.venv-local)`.

Activate it again whenever you open a new terminal to work on this project.

### 4. Install dependencies

```bash
./.venv-local/bin/python -m pip install -r requirements.txt
```

Using the environment’s Python directly ensures packages install inside it.

The `requirements.txt` file should contain:

```txt
Flask>=3.1,<4.0
```

Flask installs its dependencies, including Jinja2, automatically.
The other modules used by this application—`sqlite3`, `contextlib`,
`datetime`, and `pathlib`—are included with Python.

### 5. Run the application

```bash
./.venv-local/bin/python app.py
```

Open **http://127.0.0.1:5000** in your browser.

Keep the terminal running while using the application.
Press **Ctrl + C** to stop it.

The application creates the database tables automatically from
`schema.sql`. Saved tasks remain in `tasks.db` after restarting.

### Required project files

Ensure your checkout contains:

- `app.py`
- `schema.sql`
- `requirements.txt`
- `templates/index.html`
- `static/style.css`

### Troubleshooting

- **Externally managed environment:** Use the exact
  `./.venv-local/bin/python -m pip install ...` command above.
- **No module named flask:** Repeat the dependency installation step.
- **TemplateNotFound: index.html:** Ensure `templates/index.html`
  exists beside the application’s other project files.
- **Virtual environment creation fails:** On Ubuntu, the matching
  Python venv package may need to be installed by an administrator.

Add `.venv-local/` to `.gitignore` to keep installed packages out of Git.