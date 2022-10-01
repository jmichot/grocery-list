from src.connexion import get_db_connection
from http.client import CONFLICT, METHOD_NOT_ALLOWED, NOT_FOUND, OK, SERVICE_UNAVAILABLE
from flask import render_template, jsonify, Response, request


def configure_routes(app, test=False):

    @app.route('/addOne', methods=['POST'])
    def add_one():
        product_id = request.args.get('id')
        conn = get_db_connection(test)
        res = conn.execute("""Update things set quantity=quantity+1 where id=?""", (product_id,))
        conn.commit()
        conn.close()
        if (res.rowcount == 1):
            return Response(status=OK)
        else:
            return Response(status=NOT_FOUND, response="Product not exist")


    @app.route('/removeOne', methods=['POST'])
    def remove_one():
        product_id = request.args.get('id')
        conn = get_db_connection(test)
        product_not_exist = conn.execute("""Select count(*)=0 as nb from things where id=?""", (product_id,)).fetchall()
        product_not_exist = product_not_exist[0]['nb']
        if (product_not_exist):
            return Response(status=NOT_FOUND, response="Product not exist")
        actual_quantity = conn.execute("""Select quantity from things where id=?""", (product_id,)).fetchall()
        actual_quantity = actual_quantity[0]['quantity']
        res = None
        if (actual_quantity >= 1):
            res = conn.execute("""Update things set quantity=quantity-1 where id=?""", (product_id,))
            conn.commit()
        conn.close()
        if (res == None):
            return Response(status=METHOD_NOT_ALLOWED, response="The stock is empty")
        if (res.rowcount == 1):
            return Response(status=OK)


    @app.route('/deleteAll', methods=['POST'])
    def delete_all():
        product_id = request.args.get('id')
        conn = get_db_connection(test)
        res = conn.execute("""Delete from things where id=?""", (product_id,))
        conn.commit()
        conn.close()
        if (res.rowcount == 1):
            return Response(status=OK)
        else:
            return Response(status=NOT_FOUND, response="Product not exist")


    @app.route('/modify', methods=['POST'])
    def modify():
        product_id = request.args.get('id')
        product_quatity = request.args.get('quantity')
        product_name = request.args.get('name')
        conn = get_db_connection(test)
        name_already_exist = conn.execute("""Select count(*) as nb from things where thing=?""", (product_name,)).fetchall()
        name_already_exist = name_already_exist[0]['nb']
        if (name_already_exist > 0):
            conn.close()
            return Response(status=CONFLICT, response="Product already exist")
        else :
            res = conn.execute("""Update things set thing=?, quantity=? where id=?""", (product_name, product_quatity, product_id))
            conn.commit()
            conn.close()
            if (res.rowcount == 1):
                return Response(status=OK)
            else:
                return Response(status=NOT_FOUND, response="Product not exist")


    @app.route('/add', methods=['POST'])
    def add():
        product_quatity = request.args.get('quantity')
        product_name = request.args.get('name')
        conn = get_db_connection(test)
        name_already_exist = conn.execute("""Select count(*) as nb from things where thing=?""", (product_name,)).fetchall()
        name_already_exist = name_already_exist[0]['nb']
        if (name_already_exist > 0):
            conn.close()
            return Response(status=CONFLICT, response="Product already exist")
        else :
            res = conn.execute("""Insert into things (thing, quantity) values (?, ?)""", (product_name, product_quatity))
            conn.commit()
            conn.close()
            if (res.rowcount == 1):
                return Response(status=OK)
            else:
                return Response(status=SERVICE_UNAVAILABLE)



    @app.route('/getAll')
    def get_all():
        conn = get_db_connection(test)
        things = conn.execute('SELECT * FROM things').fetchall()
        things = [tuple(row) for row in things]
        conn.close()
        return jsonify(things)


    @app.route('/')
    def index():
        return render_template('index.html')