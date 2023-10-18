import sqlite3

conn = sqlite3.connect('qq2.db')

with open('schema_sqlite.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

rows = [
    ('First post', 'Content of first post'),
    ('Second post', 'Content of second post'),
]

for title, content in rows:
    cur.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
    # ^note: we pass as parameters (vs f-strings) to prevent SQL injection

conn.commit()
conn.close()
