from src.connexion import get_db_connection
from http.client import CONFLICT, NOT_FOUND, OK, BAD_REQUEST
from flask import render_template, jsonify, Response, request

from src.dao import Dao
from src.model.product import Product


def configure_routes(app, test=False):
    dao = Dao(test=test)

    @app.route('/addOne', methods=['POST'])
    def add_one():
        try:
            product_id = int(request.args.get('id'))
            dao.addOneQuantity(product_id)
            return Response(status=OK)
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/removeOne', methods=['POST'])
    def remove_one():
        try:
            product_id = int(request.args.get('id'))
            dao.removeOneQuantity(product_id)
            return Response(status=OK)
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/deleteAll', methods=['POST'])
    def delete_all():
        try:
            product_id = int(request.args.get('id'))
            dao.deleteProductById(product_id)
            return Response(status=OK)
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/modify', methods=['POST'])
    def modify():
        try:
            product_id = int(request.args.get('id'))
            product_quantity = int(request.args.get('quantity'))
            product_name = request.args.get('name')
            product = Product(product_id, product_quantity, product_name)
            dao.modifyProduct(product)
            return Response(status=OK)
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=NOT_FOUND, response=str(e))

    @app.route('/add', methods=['POST'])
    def add():
        try:
            product_quantity = int(request.args.get('quantity'))
            product_name = request.args.get('name')
            product = Product(None, product_quantity, product_name)
            dao.addProduct(product)
            return Response(status=OK)
        except ValueError as e:
            return Response(status=BAD_REQUEST, response=str(e))
        except Exception as e:
            return Response(status=CONFLICT, response=str(e))

    @app.route('/getAll')
    def get_all():
        products = dao.getAll()
        return jsonify(products)

    @app.route('/')
    def index():
        return render_template('index.html')
