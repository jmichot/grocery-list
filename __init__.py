import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    things = conn.execute('SELECT * FROM things').fetchall()
    conn.close()
    return render_template('index.html', things=things)

if __name__ == '__main__':
  app.run()