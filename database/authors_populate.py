import sqlite3

conn = sqlite3.connect("authors.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE authors (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    affiliation TEXT NOT NULL
);             
""")

cursor.execute("""
INSERT INTO authors (name, affiliation)
VALUES ("Felipe Boff Nunes",
        "Pontificia Catolica Universidade do Rio Grande do Sul")               
""")

conn.commit()

conn.close()