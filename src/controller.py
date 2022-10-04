from src.connexion import get_db_connection
from http.client import CONFLICT, NOT_FOUND, OK
from flask import render_template, jsonify, Response, request

from src.dao import Dao
from src.model.product import Product


def configure_routes(app, test=False):
    dao = Dao(test=test)

    @app.route('/addOne', methods=['POST'])
    def add_one():
        product_id = request.args.get('id')
        try:
            dao.addOneQuantity(product_id)
            return Response(status=OK)
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))


    @app.route('/removeOne', methods=['POST'])
    def remove_one():
        product_id = request.args.get('id')
        try:
            dao.removeOneQuantity(product_id)
            return Response(status=OK)
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))


    @app.route('/deleteAll', methods=['POST'])
    def delete_all():
        product_id = request.args.get('id')
        try:
            dao.deleteProductById(product_id)
            return Response(status=OK)
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/modify', methods=['POST'])
    def modify():
        product_id = request.args.get('id')
        product_quantity = request.args.get('quantity')
        product_name = request.args.get('name')
        product = Product(product_id, product_quantity, product_name)
        try:
            dao.modifyProduct(product)
            return Response(status=OK)
        except Exception as e:
            return Response(status=CONFLICT, response=str(e))


    @app.route('/add', methods=['POST'])
    def add():
        product_quatity = request.args.get('quantity')
        product_name = request.args.get('name')
        product = Product(None, product_quatity, product_name)
        try:
            dao.addProduct(product)
            return Response(status=OK)
        except Exception as e:
            return Response(status=CONFLICT, response=str(e))



    @app.route('/getAll')
    def get_all():
        products = dao.getAll()
        return jsonify(products)


    @app.route('/')
    def index():
        return render_template('index.html')