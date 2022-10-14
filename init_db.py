import sqlite3
import sys


def reset_db(test=False):
    if test:
        connection = sqlite3.connect('databasetest.db')
    else:
        connection = sqlite3.connect('database.db')

    with open('D:\MesDocuments\Documents\COURS\MASTER\grocery-list\schema.sql') as f:
        connection.executescript(f.read())


if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
