import sqlite3

def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
    except sqlite3.error as e:
        print(e)
    return conn