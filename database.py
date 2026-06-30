import sqlite3

conn = sqlite3.connect("students.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
department TEXT,
cgpa REAL,
status TEXT,
email TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS admin(
username TEXT,
password TEXT
)
""")

cur.execute("SELECT * FROM admin")

if cur.fetchone() is None:
    cur.execute("INSERT INTO admin VALUES('admin','admin123')")

# Drives Table

cur.execute("""
CREATE TABLE IF NOT EXISTS drives(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    drive_date TEXT NOT NULL,
    eligibility REAL NOT NULL,
    venue TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database Ready")