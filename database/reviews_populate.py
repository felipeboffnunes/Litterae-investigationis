import sqlite3

conn = sqlite3.connect("reviews.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE reviews (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    authors TEXT NOT NULL,
    tags TEXT NOT NULL,
    description TEXT NOT NULL
);             
""")

cursor.execute("""
INSERT INTO reviews (name, authors, tags, description)
VALUES ("Code Summarization SLR",
        "Felipe Boff Nunes, Afonso Henrique Correa de Sales",
        "code summarization, neural networks, deep learning",
        "A SLR searching for the state-of-art algorithms for
        code summarization")               
""")

conn.commit()

conn.close()