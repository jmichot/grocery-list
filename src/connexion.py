import sqlite3

def get_db_connection(test=False): # pragma: no mutate
    path = 'database.db' # pragma: no mutate
    if test:
        path = 'databasetest.db' # pragma: no mutate
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
    except sqlite3.error as e:
        print(e)
    return conn