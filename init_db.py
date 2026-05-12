import sqlite3

DB_NAME = "todolist.db"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# new table
cur.execute("DROP TABLE IF EXISTS entries")
cur.execute("DROP TABLE IF EXISTS users")

cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    what_to_do TEXT NOT NULL,
    due_date TEXT,
    status TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()

print("Database initialized.")
