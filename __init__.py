from http.client import CONFLICT, NOT_FOUND, OK
import sqlite3
import init_db
from flask import Flask, render_template, jsonify, Response, request

app = Flask(__name__)

def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/addOne', methods=['POST'])
def add_one():
    product_id = request.args.get('id')
    conn = get_db_connection()
    res = conn.execute("""Update things set quantity=quantity+1 where id=?""", product_id)
    conn.commit()
    conn.close()
    if (res.rowcount == 1):
        return Response(status=OK)
    else:
        return Response(status=NOT_FOUND)


@app.route('/removeOne', methods=['POST'])
def remove_one():
    product_id = request.args.get('id')
    conn = get_db_connection()
    actual_quantity = conn.execute("""Select quantity from things where id=?""", product_id).fetchall()
    actual_quantity = actual_quantity[0]['quantity']
    if (actual_quantity >= 1):
        res = conn.execute("""Update things set quantity=quantity-1 where id=?""", product_id)
        conn.commit()
    conn.close()
    if (res.rowcount == 1):
        return Response(status=OK)
    else:
        return Response(status=NOT_FOUND)


@app.route('/deleteAll', methods=['POST'])
def delete_all():
    product_id = request.args.get('id')
    conn = get_db_connection()
    res = conn.execute("""Delete from things where id=?""", product_id)
    conn.commit()
    conn.close()
    if (res.rowcount == 1):
        return Response(status=OK)
    else:
        return Response(status=NOT_FOUND)


@app.route('/modify', methods=['POST'])
def modify():
    product_id = request.args.get('id')
    product_quatity = request.args.get('quantity')
    product_name = request.args.get('name')
    conn = get_db_connection()
    name_already_exist = conn.execute("""Select count(*) as nb from things where thing=?""", (product_name,)).fetchall()
    name_already_exist = name_already_exist[0]['nb']
    if (name_already_exist > 0):
        conn.close()
        return Response(status=CONFLICT)
    else :
        res = conn.execute("""Update things set thing=?, quantity=? where id=?""", (product_name, product_quatity, product_id))
        conn.commit()
        conn.close()
        if (res.rowcount == 1):
            return Response(status=OK)
        else:
            return Response(status=NOT_FOUND)



@app.route('/getAll')
def get_all():
    conn = get_db_connection()
    things = conn.execute('SELECT * FROM things').fetchall()
    things = [tuple(row) for row in things]
    conn.close()
    return jsonify(things)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db
    app.run()