import sqlite3
from pathlib import Path

# Locate the database and schema files
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "tasks.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


# Connect to the database
connection = sqlite3.connect(DATABASE_PATH)

# Enable foreign-key enforcement
connection.execute("PRAGMA foreign_keys = ON")

# Read the SQL schema
schema = SCHEMA_PATH.read_text(encoding="utf-8")

# Create the tables and indexes
connection.executescript(schema)

# Save the changes
connection.commit()

# Close the connection
connection.close()

print("Database created successfully!")