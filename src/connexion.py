import sqlite3

def get_db_connection(test=False):
    conn = None
    try:
        if test:
            conn = sqlite3.connect('databasetest.db')
        else:
            conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
    except sqlite3.error as e:
        print(e)
    return conn