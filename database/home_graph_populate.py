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

cursor.execute("""
INSERT INTO papers (title, authors, doi, abstract, target)
VALUES ("Code summarization: Systematic Literature Review",
        "Felipe Boff Nunes, Afonso Henrique Correa de Sales",
        "a9as83019312303", "This paper talks about Code
        summarization and the state-of-art algorithms.",
        "1un13n212122n12b")               
""")

cursor.execute("""
INSERT INTO papers (title, authors, doi, abstract)
VALUES ("Code summarization with Neural Networks",
        "Xin Yao, Antony Debo",
        "1un13n212122n12b", "We implemented a very good code
        summarization neural network.")               
""")

cursor.execute("""
INSERT INTO papers (title, authors, doi, abstract, target)
VALUES ("Deep Code Summarization",
        "Yun Zi, Antony Debo",
        "assgage323dsf4", "We implemented a very good code
        summarization neural network.",
        "a9as83019312303")               
""")

cursor.execute("""
INSERT INTO papers (title, authors, doi, abstract, target)
VALUES ("Code Clone Detection",
        "Yun Zi, Kolin Malone",
        "asfjgd7831k3132", "We implemented a very good code
        clone detection system.",
        "assgage323dsf4")               
""")

conn.commit()

conn.close()