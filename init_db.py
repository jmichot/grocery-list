import sqlite3
import sys
from os.path import exists


def reset_db(test=False):
    path = 'database.db'
    if test:
        path = 'databasetest.db'

    file_exists = exists(path)
    if not file_exists:
        raise FileNotFoundError

    connection = sqlite3.connect(path)
    with open('schema.sql') as f:
        connection.executescript(f.read())

if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
