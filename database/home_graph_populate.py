import sqlite3

conn = sqlite3.connect("home_graph.db")

cursor = conn.cursor()

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

conn.commit()

conn.close()