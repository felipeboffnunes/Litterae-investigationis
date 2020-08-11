import sqlite3
import pandas as pd

def home_graph():
    conn = sqlite3.connect("./database/home_graph.db")
    
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM papers;
    """)
        
    return cursor.fetchall()
    
def review_df():
    conn = sqlite3.connect("./database/reviews.db")

    df = pd.read_sql_query("SELECT * from reviews;", conn)
    
    return df