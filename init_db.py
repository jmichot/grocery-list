import sqlite3


def reset_db():
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