import sqlite3

conn = sqlite3.connect("home_graph.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE papers (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT NOT NULL,
    doi TEXT NOT NULL,
    abstract TEXT NOT NULL,
    target TEXT
);             
""")


conn.close()