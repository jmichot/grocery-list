import sqlite3
import sys


def reset_db(test=False):
    if test:
        connection = sqlite3.connect('databasetest.db')
    else:
        connection = sqlite3.connect('database.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    cur.execute("INSERT INTO things (quantity, thing) VALUES (?, ?)",
                (3, 'Tomates')
                )

    cur.execute("INSERT INTO things (quantity, thing) VALUES (?, ?)",
                (30, 'Feuilles')
                )

    connection.commit()
    connection.close()  


if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
