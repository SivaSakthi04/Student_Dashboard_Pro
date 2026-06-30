import sqlite3

conn = sqlite3.connect("students.db")

cur = conn.cursor()

cur.execute("PRAGMA table_info(drives)")

print(cur.fetchall())

conn.close()