import sqlite3

def home_graph():
    conn = sqlite3.connect("./database/home_graph.db")
    
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM papers;
    """)
        
    return cursor.fetchall()
    